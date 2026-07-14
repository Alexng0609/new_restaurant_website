"""Keeps real Django permissions in sync with CustomUser.role.

`role` alone doesn't stop anyone from typing /admin/ URLs directly - is_staff
only grants login to /admin/, actual per-model permission comes from Django's
Group/Permission system. This signal means: change a user's role in the admin,
their group membership (and therefore their actual edit rights) updates
automatically, with no manual "add to group" step required.
"""

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser

MANAGER_GROUP_NAME = "Managers"


@receiver(post_save, sender=CustomUser)
def sync_manager_group(sender, instance, **kwargs):
    group, _ = Group.objects.get_or_create(name=MANAGER_GROUP_NAME)
    if instance.role == CustomUser.ROLE_MANAGER:
        instance.groups.add(group)
    else:
        instance.groups.remove(group)

    # Superusers are always staff regardless of role - never demote them.
    if instance.is_superuser:
        return

    should_be_staff = instance.role in (CustomUser.ROLE_STAFF, CustomUser.ROLE_MANAGER)
    if instance.is_staff != should_be_staff:
        CustomUser.objects.filter(pk=instance.pk).update(is_staff=should_be_staff)
