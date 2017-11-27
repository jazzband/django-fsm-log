from django_fsm_log.models import StateLog
import pytest


def test_for_queryset_method_returns_only_logs_for_provided_object(article, article2):
    article2.submit()

    article.submit()
    article.publish()

    assert len(StateLog.objects.for_(article)) == 2
    for log in StateLog.objects.for_(article):
        assert article == log.content_object


@pytest.fixture
def create_kwargs(user, article):
    return {
        'by': user,
        'state': 'submitted',
        'transition': 'submit',
        'content_object': article
    }


@pytest.mark.pending_objects
def test_get_cache_key_for_object_returns_correctly_formatted_string(article):
    expected_result = 'StateLog:{}:{}'.format(
        article.__class__.__name__,
        article.pk
    )
    result = StateLog.pending_objects._get_cache_key_for_object(article)
    assert result == expected_result


@pytest.mark.pending_objects
def test_create_pending_sets_cache_item(article, create_kwargs, mocker):
    mock_cache = mocker.patch('django_fsm_log.managers.cache')
    expected_cache_key = StateLog.pending_objects._get_cache_key_for_object(article)
    StateLog.pending_objects.create(**create_kwargs)
    cache_key = mock_cache.set.call_args_list[0][0][0]
    cache_object = mock_cache.set.call_args_list[0][0][1]
    assert cache_key == expected_cache_key
    assert cache_object.state == create_kwargs['state']
    assert cache_object.transition == create_kwargs['transition']
    assert cache_object.content_object == create_kwargs['content_object']
    assert cache_object.by == create_kwargs['by']


@pytest.mark.pending_objects
def test_create_returns_correct_state_log(mocker, create_kwargs):
    mocker.patch('django_fsm_log.managers.cache')
    log = StateLog.pending_objects.create(**create_kwargs)
    assert log.state == create_kwargs['state']
    assert log.transition == create_kwargs['transition']
    assert log.content_object == create_kwargs['content_object']
    assert log.by == create_kwargs['by']


@pytest.mark.pending_objects
def test_commit_for_object_saves_log(mocker, article, create_kwargs):
    mock_cache = mocker.patch('django_fsm_log.managers.cache')
    log = StateLog.objects.create(**create_kwargs)
    mock_cache.get.return_value = log
    StateLog.pending_objects.commit_for_object(article)
    persisted_log = StateLog.objects.order_by('-pk').all()[0]
    assert log.state == persisted_log.state
    assert log.transition == persisted_log.transition
    assert log.content_object == persisted_log.content_object
    assert log.by == persisted_log.by


@pytest.mark.pending_objects
def test_commit_for_object_deletes_pending_log_from_cache(mocker, article, create_kwargs):
    mock_cache = mocker.patch('django_fsm_log.managers.cache')
    StateLog.pending_objects.create(**create_kwargs)
    StateLog.pending_objects.commit_for_object(article)
    mock_cache.delete.assert_called_once_with(StateLog.pending_objects._get_cache_key_for_object(article))


@pytest.mark.pending_objects
def test_get_for_object_calls_cache_get_with_correct_key(mocker, create_kwargs):
    mock_cache = mocker.patch('django_fsm_log.managers.cache')
    cache_key = StateLog.pending_objects._get_cache_key_for_object(create_kwargs['content_object'])
    StateLog.pending_objects.get_for_object(create_kwargs['content_object'])
    mock_cache.get.assert_called_once_with(cache_key)
