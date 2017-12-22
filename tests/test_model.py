from django_fsm import TransitionNotAllowed
from django_fsm_log.models import StateLog
import pytest

from .models import Article, ArticleInteger


def test_get_available_state_transitions(article):
    assert len(list(article.get_available_state_transitions())) == 3


def test_get_all_state_transitions(article):
    assert len(list(article.get_all_state_transitions())) == 5


def test_log_created_on_transition(article):
    assert len(StateLog.objects.all()) == 0

    article.submit()
    article.save()

    assert len(StateLog.objects.all()) == 1


def test_log_not_created_if_transition_fails(article):
    assert len(StateLog.objects.all()) == 0

    with pytest.raises(TransitionNotAllowed):
        article.publish()

    assert len(StateLog.objects.all()) == 0


def test_by_is_set_when_passed_into_transition(article, user):
    article.submit(by=user)

    log = StateLog.objects.all()[0]
    assert user == log.by


def test_by_is_none_when_not_set_in_transition(article):
    article.submit()

    log = StateLog.objects.all()[0]
    assert log.by is None


def test_description_is_set_when_passed_into_transition(article):
    description = "Lorem ipsum"
    article.submit(description=description)

    log = StateLog.objects.all()[0]
    assert description == log.description


def test_description_is_none_when_not_set_in_transition(article):
    article.submit()

    log = StateLog.objects.all()[0]
    assert log.description is None


def test_description_can_be_mutated_by_the_transition(article):
    description = "Sed egestas dui"
    article.submit_inline_description_change(change_to=description)

    log = StateLog.objects.all()[0]
    assert description == log.description


def test_logged_state_is_new_state(article):
    article.submit()

    log = StateLog.objects.all()[0]
    assert log.state == 'submitted'


def test_logged_transition_is_name_of_transition_method(article):
    article.submit()

    log = StateLog.objects.all()[0]
    assert log.transition == 'submit'


def test_logged_content_object_is_instance_being_transitioned(article):
    article.submit()

    log = StateLog.objects.all()[0]
    assert log.content_object == article


def test_get_display_state(article):
    article.submit()
    article.save()

    log = StateLog.objects.latest()
    article = Article.objects.get(pk=article.pk)

    assert log.get_state_display() == article.get_state_display()

    article.publish()
    article.save()

    log = StateLog.objects.latest()

    article = Article.objects.get(pk=article.pk)

    assert log.get_state_display() == article.get_state_display()


def test_get_display_state_with_integer(article_integer):
    article_integer.change_to_two()
    article_integer.save()

    log = StateLog.objects.latest()
    article_integer = ArticleInteger.objects.get(pk=article_integer.pk)

    assert log.get_state_display() == article_integer.get_state_display()
