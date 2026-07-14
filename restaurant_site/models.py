from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator
from decimal import Decimal

from .localization import localized_text


class Category(models.Model):
    """Menu categories (e.g., Appetizers, Main Course, Desserts, Drinks)"""

    name = models.CharField(max_length=100)
    name_en = models.CharField(
        max_length=100,
        blank=True,
        help_text="English category name (optional). Falls back to Vietnamese name.",
    )
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Display order")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_localized_name(self):
        """Category names always stay in Vietnamese."""
        return self.name


class MenuItem(models.Model):
    """Menu items available for order"""

    name = models.CharField(max_length=200, help_text="Vietnamese name")
    name_en = models.CharField(
        max_length=200,
        blank=True,
        help_text="Unused — menu item names are always shown in Vietnamese.",
    )
    description = models.TextField(help_text="Vietnamese description")
    description_en = models.TextField(
        blank=True,
        help_text="English description (optional). Falls back to Vietnamese description.",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=0, validators=[MinValueValidator(Decimal("0"))]
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )
    image = models.ImageField(upload_to="menu_items/", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} - {self.price:,.0f} ₫"

    def get_localized_name(self):
        """Menu item names always stay in Vietnamese."""
        return self.name

    def get_localized_description(self):
        return localized_text(self.description, self.description_en)


class NewsFeed(models.Model):
    """Restaurant news, announcements, and promotions with video support"""

    title = models.CharField(max_length=200, help_text="Vietnamese title")
    title_en = models.CharField(
        max_length=200,
        blank=True,
        help_text="English title (optional). Falls back to Vietnamese title.",
    )
    content = models.TextField(help_text="Vietnamese content")
    content_en = models.TextField(
        blank=True,
        help_text="English content (optional). Falls back to Vietnamese content.",
    )
    image = models.ImageField(upload_to="news/", blank=True, null=True)

    video = models.FileField(
        upload_to="news/videos/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "mov", "avi", "webm"])
        ],
        help_text="Upload video (MP4, MOV, AVI, or WebM format)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "News Feed"
        verbose_name_plural = "News Feeds"

    def __str__(self):
        return self.title

    def has_media(self):
        """Check if news has either image or video"""
        return bool(self.image or self.video)

    def get_localized_title(self):
        """News titles always stay in Vietnamese."""
        return self.title

    def get_localized_content(self):
        return localized_text(self.content, self.content_en)
