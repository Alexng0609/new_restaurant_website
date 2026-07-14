from django import forms
from django.utils.translation import gettext_lazy as _

from .models import MenuItem, NewsFeed


class NewsFeedForm(forms.ModelForm):
    class Meta:
        model = NewsFeed
        fields = [
            "title",
            "content",
            "content_en",
            "image",
            "video",
        ]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 6, "class": "form-control"}),
            "content_en": forms.Textarea(attrs={"rows": 6, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": _("Title (Vietnamese)"),
            "content": _("Content (Vietnamese)"),
            "content_en": _("Content (English)"),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            "name",
            "description",
            "description_en",
            "price",
            "category",
            "image",
            "is_available",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "description_en": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": _("Item name (Vietnamese)"),
            "description": _("Description (Vietnamese)"),
            "description_en": _("Description (English)"),
        }
