"""Role helpers for staff/manager permissions.

Three effective levels, from lowest to highest:
- staff:    is_staff=True, role="staff"   -> sees Order page only
- manager:  is_staff=True, role="manager" -> manager-level actions (e.g. skip cancel code)
- admin:    is_superuser=True             -> everything

Use these helpers instead of checking user.role directly, so the superuser
override lives in one place.
"""


def get_staff_role(user):
    """Returns 'admin', 'manager', 'staff', or None (not staff at all)."""
    if not user.is_authenticated or not user.is_staff:
        return None
    if user.is_superuser:
        return "admin"
    if user.role == "manager":
        return "manager"
    if user.role == "staff":
        return "staff"
    return None


def is_manager_or_admin(user):
    """True for managers and superusers - used anywhere a normal staff member
    needs extra permission (e.g. skipping the cancel-order admin code)."""
    return get_staff_role(user) in ("manager", "admin")
