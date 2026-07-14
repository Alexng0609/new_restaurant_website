from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Drop-in replacement for Django's default User. Extends it (doesn't
    replace fields like username/password/email) so everything you already
    know about auth still works - this just gives us room to grow:
    role for staff tiers now, points/phone for the rewards program later.
    """

    ROLE_CUSTOMER = "customer"
    ROLE_STAFF = "staff"
    ROLE_MANAGER = "manager"
    ROLE_CHOICES = [
        (ROLE_CUSTOMER, "Khách hàng"),
        (ROLE_STAFF, "Nhân viên"),
        (ROLE_MANAGER, "Quản lý"),
    ]

    # Only meaningful when is_staff=True. Regular customers stay "customer"
    # and this field is otherwise ignored for them - is_staff/is_superuser
    # remain the actual permission gates, role just distinguishes staff tiers.
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)

    phone_number = models.CharField(max_length=20, blank=True)
    points = models.PositiveIntegerField(default=0, help_text="Điểm thưởng tích lũy")

    def __str__(self):
        return self.username
