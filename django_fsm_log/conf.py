from django.conf import settings
from appconf import AppConf

class DjangoFSMLogConf(AppConf):
    CACHE_BACKEND = 'django_fsm_log.backends.SimpleBackend'
