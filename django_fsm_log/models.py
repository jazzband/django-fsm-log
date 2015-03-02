# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django_fsm_log.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from django_fsm.signals import pre_transition, post_transition
from django_fsm import FSMFieldMixin

from .managers import StateLogManager
from django.utils.module_loading import import_by_path


@python_2_unicode_compatible
class StateLog(models.Model):
    timestamp = models.DateTimeField(default=now)
    by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=True, null=True)
    state = models.CharField(max_length=255, db_index=True)
    transition = models.CharField(max_length=255)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = StateLogManager()

    def __str__(self):
        return '{} - {} - {}'.format(
            self.timestamp,
            self.content_object,
            self.transition
        )

    def get_state_display(self):
        fsm_obj = self.content_object
        for field in fsm_obj._meta.fields:
            if isinstance(field, FSMFieldMixin):
                display_method = 'get_{field}_display'.format(field=field.name)
                return getattr(fsm_obj, display_method)()

try:
    import django.apps
except: # django < 1.7
    backend = import_by_path(settings.DJANGO_FSM_LOG_STORAGE_METHOD)
    backend.setup_model(StateLog)

    pre_transition.connect(backend.pre_transition_callback)
    post_transition.connect(backend.post_transition_callback)
