# Add these to your existing forms.py (create it if you don't have one yet).
# Adjust the field list if your actual models have different/extra fields.

from django import forms
from .models import NewsFeed, MenuItem


class NewsFeedForm(forms.ModelForm):
    class Meta:
        model = NewsFeed
        fields = ["title", "content", "image", "video"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 6}),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "description", "price", "category", "image", "is_available"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
