from django.contrib.auth import get_user_model
from django_fsm_log.managers import PendingStateLogManager
from django_fsm_log.models import StateLog
import pytest

from .models import Article


@pytest.fixture
def article(db, request, settings):
    if 'ignore_article' in request.keywords:
        settings.DJANGO_FSM_LOG_IGNORED_MODELS = ['tests.models.Article']
    return Article.objects.create(state='draft')


@pytest.fixture
def article2(db):
    return Article.objects.create(state='draft')


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='jacob', password='password')


@pytest.fixture(autouse=True)
def pending_objects(db, request):
    if 'pending_objects' in request.keywords:
        if not hasattr(StateLog, 'pending_objects'):
            StateLog.add_to_class('pending_objects', PendingStateLogManager())
