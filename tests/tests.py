from django.test import TestCase
from django.contrib.auth import get_user_model
from django_fsm_log.models import StateLog
from .models import Article

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
