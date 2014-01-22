from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now
from django.core.cache import cache

from django_fsm.signals import pre_transition, post_transition

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

    @staticmethod
    def get_cache_key_for_object(obj):
        return 'StateLog:{}:{}'.format(
            obj.__class__.__name__,
            obj.pk
        )

    def __unicode__(self):
        return '{} - {} - {}'.format(
            self.timestamp,
            self.content_object,
            self.transition
        )


def pre_transition_callback(sender, instance, name, source, target, **kwargs):
    state_log = StateLog(
        by=getattr(instance, 'by', None),
        state=target,
        transition=name,
        content_object=instance,
    )
    cache_key = StateLog.get_cache_key_for_object(instance)
    cache.set(cache_key, state_log)


def post_transition_callback(sender, instance, name, source, target, **kwargs):
    cache_key = StateLog.get_cache_key_for_object(instance)
    state_log = cache.get(cache_key)
    state_log.save()
    cache.set(cache_key, state_log)

pre_transition.connect(pre_transition_callback)
post_transition.connect(post_transition_callback)
