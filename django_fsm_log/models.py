from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now
from django_fsm import FSMFieldMixin, FSMIntegerField

from .conf import settings
from .managers import StateLogManager


class StateLog(models.Model):
    timestamp = models.DateTimeField(default=now)
    by = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    source_state = models.CharField(max_length=255, db_index=True, null=True, blank=True, default=None)
    state = models.CharField("Target state", max_length=255, db_index=True)
    transition = models.CharField(max_length=255)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    description = models.TextField(blank=True, null=True)

    objects = StateLogManager()

    class Meta:
        get_latest_by = "timestamp"

    def __str__(self):
        return f"{self.timestamp} - {self.content_object} - {self.transition}"

    def get_state_display(self, field_name="state"):
        fsm_cls = self.content_type.model_class()
        for field in fsm_cls._meta.fields:
            state = getattr(self, field_name)
            if isinstance(field, FSMIntegerField):
                state_display = dict(field.flatchoices).get(int(state), state)
                return str(state_display)
            elif isinstance(field, FSMFieldMixin):
                state_display = dict(field.flatchoices).get(state, state)
                return str(state_display)

    def get_source_state_display(self):
        return self.get_state_display("source_state")
