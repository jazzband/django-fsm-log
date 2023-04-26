import typing

from django.utils.module_loading import import_string

from django_fsm_log.conf import settings

from .helpers import FSMLogDescriptor

if typing.TYPE_CHECKING:
    import django_fsm_log.models


def _get_concrete_model() -> typing.Type["django_fsm_log.models.PersistedTransitionMixin"]:
    return import_string(settings.DJANGO_FSM_LOG_CONCRETE_MODEL)


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
        from .managers import PendingPersistedTransitionManager

        model.add_to_class("pending_objects", PendingPersistedTransitionManager())

    @staticmethod
    def pre_transition_callback(sender, instance, name, source, target, **kwargs):
        klass = _get_concrete_model()

        return _pre_transition_callback(sender, instance, name, source, target, klass.pending_objects, **kwargs)

    @staticmethod
    def post_transition_callback(sender, instance, name, source, target, **kwargs):
        klass = _get_concrete_model()

        klass.pending_objects.commit_for_object(instance)


class SimpleBackend(BaseBackend):
    @staticmethod
    def setup_model(model):
        pass

    @staticmethod
    def pre_transition_callback(sender, **kwargs):
        pass

    @staticmethod
    def post_transition_callback(sender, instance, name, source, target, **kwargs):
        klass = _get_concrete_model()

        return _pre_transition_callback(sender, instance, name, source, target, klass.objects, **kwargs)


if settings.DJANGO_FSM_LOG_STORAGE_METHOD == "django_fsm_log.backends.CachedBackend":
    from django.core.cache import caches

    cache = caches[settings.DJANGO_FSM_LOG_CACHE_BACKEND]
else:
    cache = None
