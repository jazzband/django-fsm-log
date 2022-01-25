from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import F

from .models import StateLog

__all__ = ("StateLogInline",)


class StateLogInline(GenericTabularInline):
    model = StateLog
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
