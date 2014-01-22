from django.test import TestCase
from django_fsm.db.fields import TransitionNotAllowed
from django_fsm_log.models import StateLog, post_transition_callback, pre_transition_callback
from .models import Article
from mock import patch

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

class StateLogModelTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(state='draft')
        self.user = User.objects.create_user(username='jacob', password='password')

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

    def test_get_pending_cache_key_for_object_returns_correctly_formatted_string(self):
        expected_result = 'StateLog:{}:{}'.format(
            self.article.__class__.__name__,
            self.article.pk
        )
        result = StateLog.get_pending_cache_key_for_object(self.article)
        self.assertEqual(result, expected_result)

    @patch('django_fsm_log.models.cache')
    def test_pre_transition_callback__pending_state_log(self, mock_cache):
        cache_key = StateLog.get_pending_cache_key_for_object(self.article)
        pre_transition_callback(self.article, self.article, 'mytransition', 'mysource', 'mytarget')
        expected_cache_object = StateLog.objects.create(
            by=None,
            state='mytarget',
            transition='mytransition',
            content_object=self.article
        )
        cache_key = mock_cache.set.call_args_list[0][0][0]
        cache_object = mock_cache.set.call_args_list[0][0][1]

        self.assertEqual(cache_key, StateLog.get_pending_cache_key_for_object(self.article))
        self.assertEqual(cache_object.state, expected_cache_object.state)
        self.assertEqual(cache_object.transition, expected_cache_object.transition)
        self.assertEqual(cache_object.content_object, expected_cache_object.content_object)


    @patch('django_fsm_log.models.cache')
    def test_post_transition_callback_gets_and_deletes_pending_state_log(self, mock_cache):
        cache_key = StateLog.get_pending_cache_key_for_object(self.article)
        post_transition_callback(self.article, self.article, 'submit', 'unfinished', 'submitted')
        mock_cache.get.assert_called_once_with(cache_key)
        mock_cache.delete.assert_called_once_with(cache_key)



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
