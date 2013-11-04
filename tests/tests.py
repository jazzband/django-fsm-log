from django.test import TestCase
from django_fsm.db.fields import TransitionNotAllowed
from django_fsm_log.models import StateLog
from .models import Article

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
