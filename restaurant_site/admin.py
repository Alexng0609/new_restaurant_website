from django.contrib import admin

from .models import Category, MenuItem, NewsFeed


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description", "description_en")
    fieldsets = (
        (None, {"fields": ("name", "category", "price", "image", "is_available")}),
        ("Descriptions", {"fields": ("description", "description_en")}),
    )


@admin.register(NewsFeed)
class NewsFeedAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "content", "content_en")
    fieldsets = (
        (None, {"fields": ("title", "image", "video", "is_active")}),
        ("Content", {"fields": ("content", "content_en")}),
    )
