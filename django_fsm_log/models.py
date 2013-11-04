from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django_fsm.signals import post_transition

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from .managers import StateLogManager


class StateLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    by = models.ForeignKey(User, blank=True, null=True)
    state = models.CharField(max_length=255, db_index=True)
    transition = models.CharField(max_length=255)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = StateLogManager()


def transition_callback(sender, instance, name, source, target, **kwargs):
    state_log = StateLog(
        by=getattr(instance, 'by', None),
        state=target,
        transition=name,
        content_object=instance,
    )
    state_log.save()


post_transition.connect(transition_callback)
