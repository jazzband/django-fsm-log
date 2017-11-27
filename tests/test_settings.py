from django.conf import settings
from django_fsm_log.models import StateLog
import pytest


pytestmark = pytest.mark.ignore_article


def test_log_not_created_if_model_ignored(article):
    assert len(StateLog.objects.all()) == 0

    article.submit()
    article.save()

    assert len(StateLog.objects.all()) == 0


def test_log_created_on_transition_when_model_not_ignored(article):
    settings.DJANGO_FSM_LOG_IGNORED_MODELS = ['tests.models.SomeOtherModel']
    assert len(StateLog.objects.all()) == 0

    article.submit()
    article.save()

    assert len(StateLog.objects.all()) == 1
