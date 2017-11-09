# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django_fsm_log.conf import settings
from django import VERSION as django_version
if django_version < (1, 7):
    from django.contrib.contenttypes.generic import GenericForeignKey
else:
    from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.timezone import now

from django_fsm.signals import pre_transition, post_transition
from django_fsm import FSMFieldMixin

from .managers import StateLogManager


@python_2_unicode_compatible
class StateLog(models.Model):
    timestamp = models.DateTimeField(default=now)
    by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=True,
                           null=True, on_delete=models.SET_NULL)
    state = models.CharField(max_length=255, db_index=True)
    transition = models.CharField(max_length=255)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = StateLogManager()

    class Meta:
        get_latest_by = 'timestamp'

    def __str__(self):
        return '{} - {} - {}'.format(
            self.timestamp,
            self.content_object,
            self.transition
        )

    def get_state_display(self):
        fsm_cls = self.content_type.model_class()
        for field in fsm_cls._meta.fields:
            if isinstance(field, FSMFieldMixin):
                state_display = dict(field.flatchoices).get(self.state, self.state)
                return force_text(state_display, strings_only=True)

try:
    import django.apps
except ImportError:  # Django < 1.7
    from django.utils.module_loading import import_by_path
    backend = import_by_path(settings.DJANGO_FSM_LOG_STORAGE_METHOD)
    backend.setup_model(StateLog)

    pre_transition.connect(backend.pre_transition_callback)
    post_transition.connect(backend.post_transition_callback)
