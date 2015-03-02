from __future__ import unicode_literals

from django.db import models
from django_fsm_log.decorators import fsm_log_by

try:
    from django_fsm import FSMField, transition
except ImportError:   # django_fsm < 2
    from django_fsm.db.fields import FSMField, transition


class Article(models.Model):
    STATES = (
        ('draft', 'Draft'),
        ('submitted', 'Article submitted'),
        ('published', 'Article published'),
        ('deleted', 'Article deleted'),
    )

    state = FSMField(choices=STATES, default='draft', protected=True)

    @fsm_log_by
    @transition(field=state, source='draft', target='submitted')
    def submit(self, by=None):
        pass

    @fsm_log_by
    @transition(field=state, source='submitted', target='draft')
    def request_changes(self, by=None):
        pass

    @fsm_log_by
    @transition(field=state, source='submitted', target='published')
    def publish(self, by=None):
        pass

    @fsm_log_by
    @transition(field=state, source='*', target='deleted')
    def delete(self, using=None):
        pass
