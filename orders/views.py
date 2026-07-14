from accounts.utils import is_manager_or_admin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView
from datetime import timedelta
import csv

from restaurant_site.models import MenuItem

from .forms import CancelOrderForm, CheckoutForm
from .models import CartItem, Order, OrderItem
from .utils import (
    can_view_order,
    get_or_create_cart,
    grant_order_confirmation_access,
    parse_positive_int,
)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restricts a view to staff accounts. Non-staff logged-in users get a 403
    (via test_func failing); anonymous users get redirected to login first."""

    def test_func(self):
        return self.request.user.is_staff


class AddToCartView(View):
    """Adds a menu item to the current cart (guest or logged-in)."""

    def post(self, request, item_id):
        menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
        cart = get_or_create_cart(request)
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        try:
            quantity = parse_positive_int(request.POST.get("quantity", 1))
        except ValueError:
            if is_ajax:
                return JsonResponse(
                    {"success": False, "error": _("Invalid quantity.")}, status=400
                )
            messages.error(request, _("Invalid quantity."))
            return redirect(request.META.get("HTTP_REFERER") or reverse("menu"))

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, menu_item=menu_item, defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=["quantity"])

        if is_ajax:
            return JsonResponse(
                {
                    "success": True,
                    "cart_total_items": cart.total_items,
                    "message": _('"%(name)s" added to cart.') % {"name": menu_item.name},
                }
            )

        messages.success(
            request, _('"%(name)s" added to cart.') % {"name": menu_item.name}
        )
        next_url = (
            request.POST.get("next")
            or request.META.get("HTTP_REFERER")
            or reverse("menu")
        )
        return redirect(next_url)


class UpdateCartItemView(View):
    """Sets a cart item's quantity (deletes it if quantity <= 0)."""

    def post(self, request, item_id):
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        try:
            quantity = parse_positive_int(request.POST.get("quantity", 1))
        except ValueError:
            messages.error(request, _("Invalid quantity."))
            return redirect("cart_detail")

        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save(update_fields=["quantity"])

        return redirect("cart_detail")


class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart = get_or_create_cart(request)
        get_object_or_404(CartItem, id=item_id, cart=cart).delete()
        return redirect("cart_detail")


class CartDetailView(View):
    template_name = "orders/cart_detail.html"

    def get(self, request):
        cart = get_or_create_cart(request)
        return render(request, self.template_name, {"cart": cart})


class CheckoutView(FormView):
    """Collects name/email/phone/address and turns the cart into an Order."""

    template_name = "orders/checkout.html"
    form_class = CheckoutForm

    def dispatch(self, request, *args, **kwargs):
        self.cart = get_or_create_cart(request)
        if self.cart.total_items == 0:
            messages.warning(request, _("Your cart is empty."))
            return redirect("cart_detail")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = self.cart
        return context

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        if user.is_authenticated:
            initial["customer_name"] = user.get_full_name() or user.get_username()
            initial["customer_email"] = user.email
        return initial

    @transaction.atomic
    def form_valid(self, form):
        unavailable = [
            cart_item.menu_item.name
            for cart_item in self.cart.items.select_related("menu_item")
            if not cart_item.menu_item.is_available
        ]
        if unavailable:
            names = ", ".join(unavailable)
            messages.error(
                self.request,
                _("Some items are no longer available: %(names)s. Please update your cart.")
                % {"names": names},
            )
            return redirect("cart_detail")

        order = form.save(commit=False)
        order.user = self.request.user if self.request.user.is_authenticated else None
        order.total_price = self.cart.total_price
        order.save()

        for cart_item in self.cart.items.select_related("menu_item"):
            OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                item_name=cart_item.menu_item.name,
                item_price=cart_item.menu_item.price,
                quantity=cart_item.quantity,
            )

        self.cart.items.all().delete()
        grant_order_confirmation_access(self.request, order.order_number)
        return redirect("order_confirmation", order_number=order.order_number)


class OrderConfirmationView(DetailView):
    model = Order
    template_name = "orders/order_confirmation.html"
    context_object_name = "order"
    slug_field = "order_number"
    slug_url_kwarg = "order_number"

    def get_object(self, queryset=None):
        order = get_object_or_404(Order, order_number=self.kwargs["order_number"])
        if not can_view_order(self.request, order):
            raise Http404("Order not found.")
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_account_invite"] = self.object.user is None
        return context


class OrderHistoryView(LoginRequiredMixin, ListView):
    """Logged-in customers can view their past orders."""

    model = Order
    template_name = "orders/order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("items")
            .order_by("-created_at")
        )


# ---------------------------------------------------------------------------
# Staff order management ("restaurant portal")
# ---------------------------------------------------------------------------


class OrderManagementView(StaffRequiredMixin, ListView):
    """Staff dashboard: every order, optionally filtered by status."""

    model = Order
    template_name = "orders/staff_order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = Order.objects.prefetch_related("items")
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Order.STATUS_CHOICES
        context["selected_status"] = self.request.GET.get("status")
        return context


class AdvanceOrderStatusView(StaffRequiredMixin, View):
    """Moves an order to the next step in the pipeline (Pending -> ... -> Delivered)."""

    def post(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        if order.status in (Order.STATUS_CANCELLED, Order.STATUS_DELIVERED):
            messages.warning(
                request,
                _("Order #%(number)s cannot be advanced further.")
                % {"number": order.order_number},
            )
            return redirect(request.POST.get("next") or "staff_order_list")

        next_status = order.get_next_status()
        if next_status:
            order.status = next_status
            order.save(update_fields=["status"])
            messages.success(
                request,
                _("Order #%(number)s -> %(status)s")
                % {"number": order.order_number, "status": order.get_status_display()},
            )
        else:
            messages.info(
                request,
                _("Order #%(number)s cannot be advanced further.")
                % {"number": order.order_number},
            )
        return redirect(request.POST.get("next") or "staff_order_list")


class CancelOrderStatusView(StaffRequiredMixin, FormView):
    """Cancelling requires a reason (always) and, unless request.user is a
    superuser, the shared admin code too - see CancelOrderForm."""

    template_name = "orders/cancel_order.html"
    form_class = CancelOrderForm

    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, order_number=kwargs["order_number"])
        if self.order.status in (Order.STATUS_CANCELLED, Order.STATUS_DELIVERED):
            messages.warning(
                request,
                _("Order #%(number)s cannot be cancelled in its current status.")
                % {"number": self.order.order_number},
            )
            return redirect("staff_order_list")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["require_code"] = not is_manager_or_admin(self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.order
        return context

    def form_valid(self, form):
        self.order.status = Order.STATUS_CANCELLED
        self.order.cancellation_reason = form.cleaned_data["reason"]
        self.order.cancelled_at = timezone.now()
        self.order.cancelled_by = self.request.user
        self.order.save(
            update_fields=[
                "status",
                "cancellation_reason",
                "cancelled_at",
                "cancelled_by",
            ]
        )
        messages.success(
            self.request,
            _("Order #%(number)s has been cancelled.")
            % {"number": self.order.order_number},
        )
        self._next_url = self.request.POST.get("next")
        return super().form_valid(form)

    def get_success_url(self):
        return self._next_url or reverse("staff_order_list")


PERIOD_CHOICES = [
    ("today", _lazy("Today")),
    ("week", _lazy("This Week")),
    ("month", _lazy("This Month")),
    ("year", _lazy("This Year")),
]

VALID_PERIODS = {value for value, _ in PERIOD_CHOICES}


def get_report_period(request):
    """Return (period_key, start_datetime) for report filters."""
    period = request.GET.get("period", "today")
    now = timezone.now()

    if period == "week":
        start = now - timedelta(days=7)
    elif period == "month":
        start = now - timedelta(days=30)
    elif period == "year":
        start = now - timedelta(days=365)
    else:
        period = "today"
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if period not in VALID_PERIODS:
        period = "today"
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    return period, start


def get_period_orders(start):
    return (
        Order.objects.filter(created_at__gte=start)
        .select_related("user", "cancelled_by")
        .prefetch_related("items")
        .order_by("-created_at")
    )


def get_translated_period_choices():
    """Eagerly translate period labels for templates."""
    return [(value, _(label)) for value, label in PERIOD_CHOICES]


class ReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Admin-only sales/orders/top-items report, filterable by period."""

    template_name = "orders/reports.html"

    def test_func(self):
        # Matches base.html's "Báo Cáo" link, which is superuser-only.
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["period_choices"] = get_translated_period_choices()
        period, start = get_report_period(self.request)

        orders_qs = Order.objects.filter(created_at__gte=start)
        completed_orders = orders_qs.exclude(status=Order.STATUS_CANCELLED)

        revenue_agg = completed_orders.aggregate(
            total=Sum("total_price"), count=Count("id")
        )
        total_revenue = revenue_agg["total"] or 0
        completed_count = revenue_agg["count"] or 0

        # Orders by status, in the same order as STATUS_CHOICES (always shows
        # every status even if count is 0, so the template doesn't need to guess).
        status_counts = dict(
            orders_qs.values_list("status").annotate(count=Count("id"))
        )
        status_breakdown = [
            {"value": value, "label": _(label), "count": status_counts.get(value, 0)}
            for value, label in Order.STATUS_CHOICES
        ]

        top_items = (
            OrderItem.objects.filter(order__created_at__gte=start)
            .exclude(order__status=Order.STATUS_CANCELLED)
            .values("item_name")
            .annotate(
                total_qty=Sum("quantity"),
                total_revenue=Sum(
                    ExpressionWrapper(
                        F("item_price") * F("quantity"),
                        output_field=DecimalField(),
                    )
                ),
            )
            .order_by("-total_qty")[:10]
        )

        context.update(
            {
                "period": period,
                "total_orders": orders_qs.count(),
                "completed_count": completed_count,
                "cancelled_count": orders_qs.filter(
                    status=Order.STATUS_CANCELLED
                ).count(),
                "total_revenue": total_revenue,
                "avg_order_value": (
                    total_revenue / completed_count if completed_count else 0
                ),
                "status_breakdown": status_breakdown,
                "top_items": top_items,
            }
        )
        return context


class ReportDetailView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Admin-only order-by-order breakdown for a selected report period."""

    template_name = "orders/reports_detail.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period, start = get_report_period(self.request)
        orders_qs = get_period_orders(start)
        completed_orders = orders_qs.exclude(status=Order.STATUS_CANCELLED)

        revenue_agg = completed_orders.aggregate(
            total=Sum("total_price"), count=Count("id")
        )
        total_revenue = revenue_agg["total"] or 0
        completed_count = revenue_agg["count"] or 0

        context.update(
            {
                "period": period,
                "period_choices": get_translated_period_choices(),
                "orders": orders_qs,
                "total_orders": orders_qs.count(),
                "completed_count": completed_count,
                "cancelled_count": orders_qs.filter(
                    status=Order.STATUS_CANCELLED
                ).count(),
                "total_revenue": total_revenue,
                "avg_order_value": (
                    total_revenue / completed_count if completed_count else 0
                ),
            }
        )
        return context


class ReportsExportView(LoginRequiredMixin, UserPassesTestMixin, View):
    """CSV export of the same report data as ReportsView, for the selected period."""

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        period, start = get_report_period(request)
        orders_qs = get_period_orders(start)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="bao_cao_{period}_{timezone.now():%Y%m%d_%H%M}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "Mã Đơn",
                "Khách Hàng",
                "SĐT",
                "Email",
                "Trạng Thái",
                "Hình Thức",
                "Thanh Toán",
                "Tổng Tiền",
                "Ngày Đặt",
            ]
        )
        for order in orders_qs:
            writer.writerow(
                [
                    order.order_number,
                    order.customer_name,
                    order.customer_phone,
                    order.customer_email,
                    order.get_status_display(),
                    order.get_fulfillment_type_display(),
                    order.get_payment_method_display(),
                    order.total_price,
                    order.created_at.strftime("%d/%m/%Y %H:%M"),
                ]
            )
        return response
