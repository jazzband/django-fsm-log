from __future__ import unicode_literals

from django.db import models
from django_fsm_log.decorators import fsm_log_by, fsm_log_description

from django_fsm import FSMField, FSMIntegerField, transition


class Article(models.Model):
    STATES = (
        ('draft', 'Draft'),
        ('submitted', 'Article submitted'),
        ('published', 'Article published'),
        ('deleted', 'Article deleted'),
    )

    state = FSMField(choices=STATES, default='draft', protected=True)

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='draft', target='submitted')
    def submit(self, description=None, by=None):
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

    @fsm_log_by
    @fsm_log_description(allow_inline=True)
    @transition(field=state, source='draft', target='submitted')
    def submit_inline_description_change(self, change_to, description):
        description.set(change_to)
        


class ArticleInteger(models.Model):
    STATE_ONE = 1
    STATE_TWO = 2

    STATES = (
        (STATE_ONE, 'one'),
        (STATE_TWO, 'two'),
    )

    state = FSMIntegerField(choices=STATES, default=STATE_ONE)

    @fsm_log_by
    @transition(field=state, source=STATE_ONE, target=STATE_TWO)
    def change_to_two(self, by=None):
        pass
