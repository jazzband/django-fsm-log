import pytest
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string

from django_fsm_log.conf import settings
from django_fsm_log.managers import PendingPersistedTransitionManager

from .models import Article, ArticleInteger


@pytest.fixture
def article(db, request, settings):
    if "ignore_article" in request.keywords:
        settings.DJANGO_FSM_LOG_IGNORED_MODELS = ["tests.models.Article"]
    return Article.objects.create(state="draft")


@pytest.fixture
def article_integer(db, request, settings):
    return ArticleInteger.objects.create()


@pytest.fixture
def article2(db):
    return Article.objects.create(state="draft")


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="jacob", password="password")


@pytest.fixture(autouse=True)
def pending_objects(db, request):
    if "pending_objects" in request.keywords:
        model_class = import_string(settings.DJANGO_FSM_LOG_CONCRETE_MODEL)
        if not hasattr(model_class, "pending_objects"):
            model_class.add_to_class("pending_objects", PendingPersistedTransitionManager())
