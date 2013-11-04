from __future__ import unicode_literals

from django.db import models
from django_fsm.db.fields import FSMField, transition
from django_fsm_log.decorators import fsm_log_by

class Article(models.Model):
    STATES = (
        'draft',
        'submitted',
        'published',
    )

    state = FSMField(default='draft', protected=True)

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
