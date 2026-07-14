from .models import Cart, CartItem


def get_or_create_cart(request):
    """Return the current cart for this request.

    - Logged-in user -> cart tied to their account (persists across devices).
    - Guest -> cart tied to their session (session created if it doesn't exist yet).
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    if not request.session.session_key:
        request.session.create()

    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def get_cart_count(request):
    """Return total items in the current cart without creating a new cart."""
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            return 0
        cart = Cart.objects.filter(session_key=session_key).first()

    return cart.total_items if cart else 0


def merge_guest_cart_into_user(user, session_key):
    """Merge a guest session cart into the user's cart, combining line items."""
    if not session_key:
        return

    guest_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
    if not guest_cart:
        return

    user_cart, _ = Cart.objects.get_or_create(user=user)

    for guest_item in guest_cart.items.select_related("menu_item"):
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            menu_item=guest_item.menu_item,
            defaults={"quantity": guest_item.quantity},
        )
        if not created:
            user_item.quantity += guest_item.quantity
            user_item.save(update_fields=["quantity"])

    guest_cart.delete()


def parse_positive_int(value, default=1):
    """Parse a positive integer from form input, raising ValueError if invalid."""
    try:
        return max(int(value), 1)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid quantity") from exc


def grant_order_confirmation_access(request, order_number):
    """Store order number in session so guests can view their confirmation page."""
    confirmed = request.session.get("confirmed_order_numbers", [])
    if order_number not in confirmed:
        confirmed.append(order_number)
        request.session["confirmed_order_numbers"] = confirmed


def can_view_order(request, order):
    """Check whether the current request may view an order confirmation."""
    if request.user.is_authenticated and order.user_id == request.user.id:
        return True
    confirmed = request.session.get("confirmed_order_numbers", [])
    return order.order_number in confirmed
