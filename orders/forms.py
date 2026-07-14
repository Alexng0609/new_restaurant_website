from django import forms
from django.conf import settings

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        # payment_method is intentionally NOT a form field yet - only cash-on-delivery
        # works right now, so it just uses the model's default. Add it here once an
        # online gateway (VNPay/MoMo) is wired up, so customers get a real choice.
        fields = [
            "customer_name",
            "customer_email",
            "customer_phone",
            "fulfillment_type",
            "delivery_address",
            "notes",
        ]
        widgets = {
            "fulfillment_type": forms.RadioSelect,
            "delivery_address": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Optional"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fulfillment_type = cleaned_data.get("fulfillment_type")
        delivery_address = cleaned_data.get("delivery_address")

        if fulfillment_type == Order.FULFILLMENT_DELIVERY and not delivery_address:
            self.add_error("delivery_address", "Vui lòng nhập địa chỉ giao hàng.")

        return cleaned_data


class CancelOrderForm(forms.Form):
    """Used by staff to cancel an order. `require_code` is set by the view based
    on whether request.user is a superuser - non-superuser staff must enter the
    shared admin code. This is a simple placeholder for now (one shared code in
    settings); swap for per-manager codes/permissions later without changing
    the calling view much.
    """

    reason = forms.CharField(
        label="Lý do hủy đơn",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=True,
    )
    admin_code = forms.CharField(
        label="Mã xác nhận quản lý",
        widget=forms.PasswordInput(render_value=False),
        required=False,
        help_text="Chỉ cần nhập nếu bạn không phải quản lý cấp cao (superuser).",
    )

    def __init__(self, *args, require_code=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.require_code = require_code
        if not require_code:
            # Superusers don't need the field at all - drop it instead of just
            # hiding it, so the template doesn't render an unused input.
            del self.fields["admin_code"]

    def clean_admin_code(self):
        code = self.cleaned_data.get("admin_code")
        expected = getattr(settings, "ADMIN_CANCEL_CODE", None)
        if not expected:
            raise forms.ValidationError(
                "Chưa thiết lập ADMIN_CANCEL_CODE trong settings.py - liên hệ quản trị viên."
            )
        if code != expected:
            raise forms.ValidationError("Mã xác nhận không đúng.")
        return code
