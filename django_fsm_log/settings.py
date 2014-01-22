from django.conf import settings

if hasattr(settings, 'DJANGO_FSM_LOG_USE_CACHE'):
    DJANGO_FSM_LOG_USE_CACHE = settings.DJANGO_FSM_LOG_USE_CACHE
else:
    DJANGO_FSM_LOG_USE_CACHE = False
