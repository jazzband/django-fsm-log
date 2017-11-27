from django.conf import settings  # noqa:F811
from appconf import AppConf


class DjangoFSMLogConf(AppConf):
    STORAGE_METHOD = 'django_fsm_log.backends.SimpleBackend'
    CACHE_BACKEND = 'default'
    IGNORED_MODELS = []
