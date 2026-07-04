from django import forms

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
