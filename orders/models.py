import uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Cart(models.Model):
    """Shopping cart. Works for guests (session-based) and logged-in users.

    Exactly one of `session_key` / `user` is expected to be set at a time.
    When a guest later creates/logs into an account, call
    `merge_guest_cart_into(user)` to hand the cart over to them.
    """

    session_key = models.CharField(max_length=40, unique=True, null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        owner = self.user.email if self.user else f"guest:{self.session_key}"
        return f"Cart ({owner})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum((item.subtotal for item in self.items.all()), Decimal("0"))

    def merge_guest_cart_into(self, user):
        """Reassign a guest cart to a newly-registered/logged-in user."""
        self.user = user
        self.session_key = None
        self.save(update_fields=["user", "session_key"])


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(
        "restaurant_site.MenuItem",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "menu_item")

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity


def generate_order_number():
    return uuid.uuid4().hex[:10].upper()


class Order(models.Model):
    """A placed order. Guest checkout is fully supported - `user` is optional."""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_PREPARING = "preparing"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_PREPARING, "Preparing"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    FULFILLMENT_PICKUP = "pickup"
    FULFILLMENT_DELIVERY = "delivery"
    FULFILLMENT_CHOICES = [
        (FULFILLMENT_PICKUP, "Tự đến lấy"),
        (FULFILLMENT_DELIVERY, "Giao hàng"),
    ]

    PAYMENT_COD = "cash_on_delivery"
    PAYMENT_ONLINE = "online_payment"
    PAYMENT_CHOICES = [
        (PAYMENT_COD, "Thanh toán khi nhận hàng"),
        (PAYMENT_ONLINE, "Thanh toán online"),
    ]

    order_number = models.CharField(
        max_length=10, unique=True, default=generate_order_number, editable=False
    )

    # Nullable on purpose: guests can order without an account.
    # If the customer is logged in at checkout, this is set automatically.
    # If they sign up *after* ordering, link_orders_to_user() below can attach it.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    # Always stored on the order itself (not just pulled from a user profile),
    # since it's a snapshot of who/where THIS order goes to.
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)

    fulfillment_type = models.CharField(
        max_length=20, choices=FULFILLMENT_CHOICES, default=FULFILLMENT_DELIVERY
    )
    # Optional at the DB level because pickup orders don't need one -
    # CheckoutForm.clean() enforces it's filled in when fulfillment_type == delivery.
    delivery_address = models.TextField(
        blank=True, help_text="Required for delivery orders, leave blank for pickup"
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default=PAYMENT_COD
    )
    notes = models.TextField(blank=True, help_text="Special instructions for the order")

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=0, validators=[MinValueValidator(Decimal("0"))]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer_name}"

    def calculate_total(self):
        """Recompute total_price from this order's existing OrderItems.

        Useful after admin edits/refunds an order's items. NOT used at checkout -
        there we set total_price = cart.total_price before the order's first save,
        since the OrderItems don't exist yet at that point.
        """
        total = sum((item.subtotal for item in self.items.all()), Decimal("0"))
        self.total_price = total
        return total

    @classmethod
    def link_orders_to_user(cls, user):
        """Call this right after a guest creates an account (in the accounts app).
        Attaches any past guest orders placed with the same email to their new account.
        """
        return cls.objects.filter(
            user__isnull=True, customer_email__iexact=user.email
        ).update(user=user)


class OrderItem(models.Model):
    """Snapshot of a menu item at the moment of order.

    Storing item_name/item_price here (not just a FK) means past orders stay
    accurate even if the menu item's price changes later or it gets deleted.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(
        "restaurant_site.MenuItem",
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_items",
    )
    item_name = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.item_name}"

    @property
    def subtotal(self):
        return self.item_price * self.quantity
