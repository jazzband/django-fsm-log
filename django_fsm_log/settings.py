"""Settings for django-fsm-log"""
import logging
from django.conf import settings

LOG = logging.getLogger(__name__)

if not hasattr(settings, 'CACHES'):
    LOG.warning("No cache backend set in django. You will not be able to access pending StateLogs")
    DJANGO_FSM_LOG_PENDING_STATELOGS = False
else:
    DJANGO_FSM_LOG_PENDING_STATELOGS = True
