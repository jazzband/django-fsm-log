import pytest
from django_fsm import TransitionNotAllowed

from django_fsm_log.models import StateLog

from .models import Article, ArticleInteger


def test_get_available_state_transitions(article):
    assert len(list(article.get_available_state_transitions())) == 5


def test_get_all_state_transitions(article):
    assert len(list(article.get_all_state_transitions())) == 7


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


def test_log_not_created_if_target_is_none(article):
    assert len(StateLog.objects.all()) == 0

    article.validate_draft()

    assert len(StateLog.objects.all()) == 0


def test_by_is_set_when_passed_into_transition(article, user):
    article.submit(by=user)

    log = StateLog.objects.all()[0]
    assert user == log.by
    with pytest.raises(AttributeError):
        _ = article.__django_fsm_log_attr_by


def test_by_is_none_when_not_set_in_transition(article):
    article.submit()

    log = StateLog.objects.all()[0]
    assert log.by is None


def test_description_is_set_when_passed_into_transition(article):
    description = "Lorem ipsum"
    article.submit(description=description)

    log = StateLog.objects.all()[0]
    assert description == log.description
    with pytest.raises(AttributeError):
        _ = article.__django_fsm_log_attr_description


def test_description_is_none_when_not_set_in_transition(article):
    article.submit()

    log = StateLog.objects.all()[0]
    assert log.description is None


def test_description_can_be_mutated_by_the_transition(article):
    description = "Sed egestas dui"
    article.submit_inline_description_change(change_to=description)

    log = StateLog.objects.all()[0]
    assert description == log.description
    with pytest.raises(AttributeError):
        article.__django_fsm_log_attr_description  # noqa: B018


def test_default_description(article):
    article.delete()
    article.save()
    article.restore()
    article.save()

    log = StateLog.objects.all()[1]
    assert log.description == "Article restored"


def test_default_description_call_priority(article):
    article.delete()
    article.save()
    article.restore(description="Restored because of mistake")
    article.save()

    log = StateLog.objects.all()[1]
    assert log.description == "Restored because of mistake"


def test_default_description_inline_priority(article):
    article.publish_as_temporary()
    article.save()

    log = StateLog.objects.all()[0]
    assert log.description == "Article published (temporary)"


def test_logged_state_is_new_state(article):
    article.submit()

    log = StateLog.objects.all()[0]
    assert log.state == "submitted"


def test_logged_transition_is_name_of_transition_method(article):
    article.submit()

    log = StateLog.objects.all()[0]
    assert log.transition == "submit"


def test_logged_content_object_is_instance_being_transitioned(article):
    article.submit()

    log = StateLog.objects.all()[0]
    assert log.content_object == article


def test_get_display_state(article):
    article.submit()
    article.save()

    log = StateLog.objects.latest()
    article = Article.objects.get(pk=article.pk)
    prev_state = article.get_state_display()

    assert log.get_state_display() == prev_state

    article.publish()
    article.save()

    log = StateLog.objects.latest()

    article = Article.objects.get(pk=article.pk)

    assert log.get_state_display() == article.get_state_display()
    assert log.get_source_state_display() == prev_state


def test_get_display_state_with_integer(article_integer):
    article_integer.change_to_two()
    article_integer.save()

    log = StateLog.objects.latest()
    article_integer = ArticleInteger.objects.get(pk=article_integer.pk)

    assert log.get_state_display() == article_integer.get_state_display()
    # only to appease code coverage
    assert str(article_integer) == f"pk={article_integer.pk}"
