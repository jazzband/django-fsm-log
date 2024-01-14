from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string
from django_fsm.signals import post_transition, pre_transition


class DjangoFSMLogAppConfig(AppConfig):
    name = "django_fsm_log"
    verbose_name = "Django FSM Log"

    def ready(self):
        backend = import_string(settings.DJANGO_FSM_LOG_STORAGE_METHOD)
        ConcreteModel = import_string(settings.DJANGO_FSM_LOG_CONCRETE_MODEL)

        backend.setup_model(ConcreteModel)

        pre_transition.connect(backend.pre_transition_callback)
        post_transition.connect(backend.post_transition_callback)
