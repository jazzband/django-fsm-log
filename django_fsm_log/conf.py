from appconf import AppConf
from django.conf import settings  # noqa: F401


class DjangoFSMLogConf(AppConf):
    STORAGE_METHOD = "django_fsm_log.backends.SimpleBackend"
    CACHE_BACKEND = "default"
    IGNORED_MODELS = []
