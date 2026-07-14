# Add to accounts/context_processors.py (create the file if it doesn't exist yet
# — adjust the import path below if utils.py actually lives in a different app).
#
# This is the single source of truth for "what can this user see" in
# templates, instead of feeds.html, menu.html, and base.html each
# re-deriving is_staff/is_superuser/role combinations slightly differently
# (which is exactly how feeds.html ended up letting plain staff manage
# news posts — it only checked is_staff, not role).

from .utils import get_staff_role


def staff_role(request):
    """Adds `staff_role` to every template context: 'admin', 'manager',
    'staff', or None (not staff / not authenticated)."""
    return {"staff_role": get_staff_role(request.user)}
