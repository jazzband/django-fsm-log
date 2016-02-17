from unittest import skipIf

from django.conf import settings
from django.test import TestCase

from django_fsm_log.models import StateLog
from django_fsm_log.managers import PendingStateLogManager

from .models import Article
from mock import patch

try:
    from django_fsm import TransitionNotAllowed
    DJANGO_FSM_VER_1 = False
except ImportError:   # django_fsm 1.x
    DJANGO_FSM_VER_1 = True
    from django_fsm.db.fields import TransitionNotAllowed

try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class StateLogModelTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(state='draft')
        self.user = User.objects.create_user(username='jacob', password='password')

    def test_get_available_state_transitions(self):
        self.assertEqual(len(list(self.article.get_available_state_transitions())), 2)

    @skipIf(DJANGO_FSM_VER_1, 'requires django-fsm>1')
    def test_get_all_state_transitions(self):
        self.assertEqual(len(list(self.article.get_all_state_transitions())), 4)

    def test_log_created_on_transition(self):
        self.assertEqual(len(StateLog.objects.all()), 0)

        self.article.submit()
        self.article.save()

        self.assertEqual(len(StateLog.objects.all()), 1)

    def test_log_not_created_if_transition_fails(self):
        self.assertEqual(len(StateLog.objects.all()), 0)

        with self.assertRaises(TransitionNotAllowed):
            self.article.publish()
            self.article.save()

        self.assertEqual(len(StateLog.objects.all()), 0)

    def test_by_is_set_when_passed_into_transition(self):
        self.article.submit(by=self.user)

        log = StateLog.objects.all()[0]
        self.assertEqual(self.user, log.by)

    def test_by_is_none_when_not_set_in_transition(self):
        self.article.submit()

        log = StateLog.objects.all()[0]
        self.assertIsNone(log.by)

    def test_logged_state_is_new_state(self):
        self.article.submit()

        log = StateLog.objects.all()[0]
        self.assertEqual(log.state, 'submitted')

    def test_logged_transition_is_name_of_transition_method(self):
        self.article.submit()

        log = StateLog.objects.all()[0]
        self.assertEqual(log.transition, 'submit')

    def test_logged_content_object_is_instance_being_transitioned(self):
        self.article.submit()

        log = StateLog.objects.all()[0]
        self.assertEqual(log.content_object, self.article)

    def test_get_display_state(self):
        self.article.submit()
        self.article.save()

        log = StateLog.objects.latest()
        article = Article.objects.get(pk=self.article.pk)
        self.assertEqual(log.get_state_display(), article.get_state_display())

        self.article.publish()
        self.article.save()

        log = StateLog.objects.all()[0]

        article = Article.objects.get(pk=self.article.pk)
        self.assertNotEqual(log.get_state_display(), article.get_state_display())


class StateLogIgnoredModelTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(state='draft')
        self.user = User.objects.create_user(username='jacob', password='password')
        settings.DJANGO_FSM_LOG_IGNORED_MODELS = ['tests.models.Article']

    def tearDown(self):
        settings.DJANGO_FSM_LOG_IGNORED_MODELS = []

    def test_log_not_created_if_model_ignored(self):
        self.assertEqual(len(StateLog.objects.all()), 0)

        self.article.submit()
        self.article.save()

        self.assertEqual(len(StateLog.objects.all()), 0)

    def test_log_created_on_transition_when_model_not_ignored(self):
        settings.DJANGO_FSM_LOG_IGNORED_MODELS = ['tests.models.SomeOtherModel']
        self.assertEqual(len(StateLog.objects.all()), 0)

        self.article.submit()
        self.article.save()

        self.assertEqual(len(StateLog.objects.all()), 1)


class StateLogManagerTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(state='draft')
        self.user = User.objects.create_user(username='jacob', password='password')

    def test_for_queryset_method_returns_only_logs_for_provided_object(self):
        article2 = Article.objects.create(state='draft')
        article2.submit()

        self.article.submit()
        self.article.publish()

        self.assertEqual(len(StateLog.objects.for_(self.article)), 2)
        for log in StateLog.objects.for_(self.article):
            self.assertEqual(self.article, log.content_object)


class PendingStateLogManagerTests(TestCase):
    def setUp(self):
        if not hasattr(StateLog, 'pending_objects'):
            StateLog.add_to_class('pending_objects', PendingStateLogManager())
        self.article = Article.objects.create(state='draft')
        self.user = User.objects.create_user(username='jacob', password='password')
        self.create_kwargs = {
            'by': self.user,
            'state': 'submitted',
            'transition': 'submit',
            'content_object': self.article
        }

    def test_get_cache_key_for_object_returns_correctly_formatted_string(self):
        expected_result = 'StateLog:{}:{}'.format(
            self.article.__class__.__name__,
            self.article.pk
        )
        result = StateLog.pending_objects._get_cache_key_for_object(self.article)
        self.assertEqual(result, expected_result)

    @patch('django_fsm_log.managers.cache')
    def test_create_pending_sets_cache_item(self, mock_cache):
        expected_cache_key = StateLog.pending_objects._get_cache_key_for_object(self.article)
        StateLog.pending_objects.create(**self.create_kwargs)
        cache_key = mock_cache.set.call_args_list[0][0][0]
        cache_object = mock_cache.set.call_args_list[0][0][1]
        self.assertEqual(cache_key, expected_cache_key)
        self.assertEqual(cache_object.state, self.create_kwargs['state'])
        self.assertEqual(cache_object.transition, self.create_kwargs['transition'])
        self.assertEqual(cache_object.content_object, self.create_kwargs['content_object'])
        self.assertEqual(cache_object.by, self.create_kwargs['by'])

    @patch('django_fsm_log.managers.cache')
    def test_create_returns_correct_state_log(self, mock_cache):
        log = StateLog.pending_objects.create(**self.create_kwargs)
        self.assertEqual(log.state, self.create_kwargs['state'])
        self.assertEqual(log.transition, self.create_kwargs['transition'])
        self.assertEqual(log.content_object, self.create_kwargs['content_object'])
        self.assertEqual(log.by, self.create_kwargs['by'])

    @patch('django_fsm_log.managers.cache')
    def test_commit_for_object_saves_log(self, mock_cache):
        log = StateLog.objects.create(**self.create_kwargs)
        mock_cache.get.return_value = log
        StateLog.pending_objects.commit_for_object(self.article)
        persisted_log = StateLog.objects.order_by('-pk').all()[0]
        self.assertEqual(log.state, persisted_log.state)
        self.assertEqual(log.transition, persisted_log.transition)
        self.assertEqual(log.content_object, persisted_log.content_object)
        self.assertEqual(log.by, persisted_log.by)

    @patch('django_fsm_log.managers.cache')
    def test_commit_for_object_deletes_pending_log_from_cache(self, mock_cache):
        StateLog.pending_objects.create(**self.create_kwargs)
        StateLog.pending_objects.commit_for_object(self.article)
        mock_cache.delete.assert_called_once_with(StateLog.pending_objects._get_cache_key_for_object(self.article))

    @patch('django_fsm_log.managers.cache')
    def test_get_for_object_calls_cache_get_with_correct_key(self, mock_cache):
        cache_key = StateLog.pending_objects._get_cache_key_for_object(self.create_kwargs['content_object'])
        StateLog.pending_objects.get_for_object(self.create_kwargs['content_object'])
        mock_cache.get.assert_called_once_with(cache_key)
