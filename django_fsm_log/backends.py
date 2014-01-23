from django.core.cache import get_cache
from django_fsm_log.conf import settings

if settings.DJANGO_FSM_LOG_CACHE_BACKEND:
    cache = get_cache(settings.DJANGO_FSM_LOG_CACHE_BACKEND)
else:
    cache = None
