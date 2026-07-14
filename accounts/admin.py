"""accounts/admin.py - registers CustomUser with role/points visible and
editable right on the normal Django admin User page. No StaffProfile inline
needed anymore since role lives directly on CustomUser.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # UserAdmin's default fieldsets, plus our new fields grouped in their own section.
    fieldsets = UserAdmin.fieldsets + (
        ("Vai trò & Điểm thưởng", {"fields": ("role", "phone_number", "points")}),
    )
    # Shown on the "Add user" page too, so role can be set at creation time.
    add_fieldsets = UserAdmin.add_fieldsets + (("Vai trò", {"fields": ("role",)}),)
    list_display = ("username", "email", "role", "is_staff", "is_superuser")
    list_filter = UserAdmin.list_filter + ("role",)


admin.site.register(CustomUser, CustomUserAdmin)
