from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator
from decimal import Decimal


# Create your models here.
class Category(models.Model):
    """Menu categories (e.g., Appetizers, Main Course, Desserts, Drinks)"""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Display order")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Menu items available for order"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=0, validators=[MinValueValidator(Decimal("0"))]
    )  # Updated for VND - supports up to 9,999,999,999
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


class NewsFeed(models.Model):
    """Restaurant news, announcements, and promotions with video support"""

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="news/", blank=True, null=True)

    # NEW VIDEO FIELD
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
