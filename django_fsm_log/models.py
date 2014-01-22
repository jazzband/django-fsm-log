from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now

from django_fsm.signals import pre_transition, post_transition

from .backends import DJANGO_FSM_LOG_USE_CACHE
from .managers import StateLogManager


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


def pre_transition_callback(sender, instance, name, source, target, **kwargs):
    if not DJANGO_FSM_LOG_USE_CACHE:
        pass
    else:
        StateLog.objects.create_pending(
            by=getattr(instance, 'by', None),
            state=target,
            transition=name,
            content_object=instance,
        )


def post_transition_callback(sender, instance, name, source, target, **kwargs):
    if not DJANGO_FSM_LOG_USE_CACHE:
        state_log = StateLog(
            by=getattr(instance, 'by', None),
            state=target,
            transition=name,
            content_object=instance,
        )
        state_log.save()
    else:
        StateLog.objects.commit_pending_for_object(instance)

pre_transition.connect(pre_transition_callback)
post_transition.connect(post_transition_callback)
