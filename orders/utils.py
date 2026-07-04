from .models import Cart


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
