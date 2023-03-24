from warnings import warn

from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import F

from .backends import _get_concrete_model

__all__ = ("PersistedTransitionInline",)


class PersistedTransitionInline(GenericTabularInline):
    model = _get_concrete_model()
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    fields = (
        "transition",
        "source_state",
        "state",
        "by",
        "description",
        "timestamp",
    )

    def get_readonly_fields(self, request, obj=None):
        return self.fields

    def get_queryset(self, request):
        return super().get_queryset(request).order_by(F("timestamp").desc())


def StateLogInline(*args, **kwargs):
    warn(
        "StateLogInLine has been deprecated by PersistedTransitionInline.",
        DeprecationWarning,
        stacklevel=2,
    )
    return PersistedTransitionInline(*args, **kwargs)
