from __future__ import unicode_literals

from django_fsm_log.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now

from django_fsm.signals import pre_transition, post_transition

from .managers import StateLogManager, PendingStateLogManager


class StateLog(models.Model):
    timestamp = models.DateTimeField(default=now)
    by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=True, null=True)
    state = models.CharField(max_length=255, db_index=True)
    transition = models.CharField(max_length=255)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = StateLogManager()
    pending_objects = PendingStateLogManager()

    def __unicode__(self):
        return '{} - {} - {}'.format(
            self.timestamp,
            self.content_object,
            self.transition
        )


def create_pending_statelog_callback(sender, instance, name, source, target, **kwargs):
    StateLog.pending_objects.create(
        by=getattr(instance, 'by', None),
        state=target,
        transition=name,
        content_object=instance,
    )


def record_statelog_callback(sender, instance, name, source, target, **kwargs):
    state_log = StateLog(
        by=getattr(instance, 'by', None),
        state=target,
        transition=name,
        content_object=instance,
    )
    state_log.save()


def commit_statelog_callback(sender, instance, name, source, target, **kwargs):
    StateLog.pending_objects.commit_for_object(instance)


if settings.DJANGO_FSM_LOG_CACHE_BACKEND:
    pre_transition.connect(create_pending_statelog_callback)
    post_transition.connect(commit_statelog_callback)
else:
    post_transition.connect(record_statelog_callback)
