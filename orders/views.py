from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView

from restaurant_site.models import MenuItem

from .forms import CheckoutForm
from .models import CartItem, Order, OrderItem
from .utils import get_or_create_cart


class AddToCartView(View):
    """Adds a menu item to the current cart (guest or logged-in)."""

    def post(self, request, item_id):
        menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
        cart = get_or_create_cart(request)
        quantity = max(int(request.POST.get("quantity", 1)), 1)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, menu_item=menu_item, defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=["quantity"])

        messages.success(request, f"{menu_item.name} added to cart.")
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
        quantity = int(request.POST.get("quantity", 1))

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
            messages.warning(request, "Your cart is empty.")
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
        order = form.save(commit=False)
        order.user = self.request.user if self.request.user.is_authenticated else None
        # Set total_price from the cart BEFORE the first save - the cart items
        # still exist at this point, so we don't need OrderItems to exist first,
        # and total_price is never briefly unset/zero in the database.
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
        return redirect("order_confirmation", order_number=order.order_number)


class OrderConfirmationView(DetailView):
    model = Order
    template_name = "orders/order_confirmation.html"
    context_object_name = "order"
    slug_field = "order_number"
    slug_url_kwarg = "order_number"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Guests get invited to create an account (accounts app) to track
        # this and future orders + earn reward points later.
        context["show_account_invite"] = self.object.user is None
        return context
