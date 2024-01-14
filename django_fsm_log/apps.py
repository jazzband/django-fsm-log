from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string
from django_fsm.signals import post_transition, pre_transition


class DjangoFSMLogAppConfig(AppConfig):
    name = "django_fsm_log"
    verbose_name = "Django FSM Log"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        backend = import_string(settings.DJANGO_FSM_LOG_STORAGE_METHOD)
        StateLog = self.get_model("StateLog")

        backend.setup_model(StateLog)

        pre_transition.connect(backend.pre_transition_callback)
        post_transition.connect(backend.post_transition_callback)
