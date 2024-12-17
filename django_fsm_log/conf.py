from typing import List

from appconf import AppConf
from django.conf import settings  # noqa: F401


class DjangoFSMLogConf(AppConf):
    STORAGE_METHOD = "django_fsm_log.backends.SimpleBackend"
    CACHE_BACKEND = "default"
    IGNORED_MODELS: List[str] = []
    CONCRETE_MODEL: str = "django_fsm_log.models.StateLog"

    class Meta:
        prefix = "django_fsm_log"
        holder = "django_fsm_log.conf.settings"
