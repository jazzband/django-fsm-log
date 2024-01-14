import pytest
from django.conf import settings

from tests.models import PersistedTransition

pytestmark = pytest.mark.ignore_article


def test_log_not_created_if_model_ignored(article):
    assert len(PersistedTransition.objects.all()) == 0

    article.submit()
    article.save()

    assert len(PersistedTransition.objects.all()) == 0


def test_log_created_on_transition_when_model_not_ignored(article):
    settings.DJANGO_FSM_LOG_IGNORED_MODELS = ["tests.models.SomeOtherModel"]
    assert len(PersistedTransition.objects.all()) == 0

    article.submit()
    article.save()

    assert len(PersistedTransition.objects.all()) == 1
