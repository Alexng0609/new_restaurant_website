from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer_name",
            "customer_email",
            "customer_phone",
            "fulfillment_type",
            "delivery_address",
            "notes",
        ]
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "customer_email": forms.EmailInput(attrs={"class": "form-control"}),
            "customer_phone": forms.TextInput(attrs={"class": "form-control"}),
            "fulfillment_type": forms.RadioSelect,
            "delivery_address": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "notes": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": _("Optional notes"),
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "customer_name": _("Full name"),
            "customer_email": _("Email"),
            "customer_phone": _("Phone number"),
            "fulfillment_type": _("Fulfillment method"),
            "delivery_address": _("Delivery address"),
            "notes": _("Notes"),
        }

    def clean(self):
        cleaned_data = super().clean()
        fulfillment_type = cleaned_data.get("fulfillment_type")
        delivery_address = cleaned_data.get("delivery_address")

        if fulfillment_type == Order.FULFILLMENT_DELIVERY and not delivery_address:
            self.add_error(
                "delivery_address",
                _("Please enter a delivery address."),
            )

        return cleaned_data


class CancelOrderForm(forms.Form):
    reason = forms.CharField(
        label=_("Cancellation reason"),
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        required=True,
    )
    admin_code = forms.CharField(
        label=_("Manager confirmation code"),
        widget=forms.PasswordInput(render_value=False, attrs={"class": "form-control"}),
        required=False,
        help_text=_("Required unless you are a senior manager (superuser)."),
    )

    def __init__(self, *args, require_code=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.require_code = require_code
        if not require_code:
            del self.fields["admin_code"]

    def clean_admin_code(self):
        code = self.cleaned_data.get("admin_code")
        expected = getattr(settings, "ADMIN_CANCEL_CODE", None)
        if not expected:
            raise forms.ValidationError(
                _(
                    "ADMIN_CANCEL_CODE is not configured in settings — contact an administrator."
                )
            )
        if code != expected:
            raise forms.ValidationError(_("Confirmation code is incorrect."))
        return code
