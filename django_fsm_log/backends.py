from django.core.exceptions import ImproperlyConfigured
from django.core.cache import get_cache
from django.conf import settings
from .settings import DJANGO_FSM_LOG_USE_CACHE

if DJANGO_FSM_LOG_USE_CACHE:
    if hasattr(settings, 'DJANGO_FSM_LOG_CACHE_BACKEND'):
        cache = get_cache(settings.DJANGO_FSM_LOG_CACHE_BACKEND)
elif hasattr(settings, 'DJANGO_FSM_LOG_CACHE_BACKEND'):
    raise ImproperlyConfigured
else:
    cache = get_cache('default')

