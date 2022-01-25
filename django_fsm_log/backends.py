from django_fsm_log.conf import settings

from .helpers import FSMLogDescriptor


def _pre_transition_callback(sender, instance, name, source, target, manager, **kwargs):

    if BaseBackend._get_model_qualified_name__(sender) in settings.DJANGO_FSM_LOG_IGNORED_MODELS:
        return

    if target is None:
        return

    values = {
        "source_state": source,
        "state": target,
        "transition": name,
        "content_object": instance,
    }
    try:
        values["by"] = FSMLogDescriptor(instance, "by").get()
    except AttributeError:
        pass
    try:
        values["description"] = FSMLogDescriptor(instance, "description").get()
    except AttributeError:
        pass

    manager.create(**values)


class BaseBackend:
    @staticmethod
    def setup_model(model):
        raise NotImplementedError

    @staticmethod
    def pre_transition_callback(*args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def post_transition_callback(*args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def _get_model_qualified_name__(sender):
        return "{}.{}".format(sender.__module__, getattr(sender, "__qualname__", sender.__name__))


class CachedBackend(BaseBackend):
    @staticmethod
    def setup_model(model):
        from .managers import PendingStateLogManager

        model.add_to_class("pending_objects", PendingStateLogManager())

    @staticmethod
    def pre_transition_callback(sender, instance, name, source, target, **kwargs):
        from .models import StateLog

        return _pre_transition_callback(sender, instance, name, source, target, StateLog.pending_objects, **kwargs)

    @staticmethod
    def post_transition_callback(sender, instance, name, source, target, **kwargs):
        from .models import StateLog

        StateLog.pending_objects.commit_for_object(instance)


class SimpleBackend(BaseBackend):
    @staticmethod
    def setup_model(model):
        pass

    @staticmethod
    def pre_transition_callback(sender, **kwargs):
        pass

    @staticmethod
    def post_transition_callback(sender, instance, name, source, target, **kwargs):
        from .models import StateLog

        return _pre_transition_callback(sender, instance, name, source, target, StateLog.objects, **kwargs)


if settings.DJANGO_FSM_LOG_STORAGE_METHOD == "django_fsm_log.backends.CachedBackend":
    try:
        from django.core.cache import caches
    except ImportError:
        from django.core.cache import get_cache  # Deprecated, removed in 1.9.

        cache = get_cache(settings.DJANGO_FSM_LOG_CACHE_BACKEND)
    else:
        cache = caches[settings.DJANGO_FSM_LOG_CACHE_BACKEND]
else:
    cache = None
