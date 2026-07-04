# orders/context_processors.py
from .utils import get_or_create_cart


def cart_count(request):
    return {"cart_count": get_or_create_cart(request).total_items}
