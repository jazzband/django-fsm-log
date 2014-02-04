from django.conf import settings
from appconf import AppConf
from django.core.cache import get_cache


class DjangoFSMLogConf(AppConf):
    STORAGE_METHOD = 'django_fsm_log.backends.SimpleBackend'
    CACHE_BACKEND = get_cache('default')
