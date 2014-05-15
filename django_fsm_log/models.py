from __future__ import unicode_literals

from django_fsm_log.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now

from django_fsm.signals import pre_transition, post_transition

from .managers import StateLogManager
from .utils import import_class_by_path


class StateLog(models.Model):
    timestamp = models.DateTimeField(default=now)
    by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=True, null=True)
    state = models.CharField(max_length=255, db_index=True)
    transition = models.CharField(max_length=255)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = StateLogManager()

    def __unicode__(self):
        return '{} - {} - {}'.format(
            self.timestamp,
            self.content_object,
            self.transition
        )

backend = import_class_by_path(settings.DJANGO_FSM_LOG_STORAGE_METHOD)
backend.setup_model(StateLog)
pre_transition.connect(backend.pre_transition_callback)
post_transition.connect(backend.post_transition_callback)
