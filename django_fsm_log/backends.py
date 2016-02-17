from django_fsm_log.conf import settings


class BaseBackend(object):

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
        return '%s.%s' % (sender.__module__,
                          getattr(sender, '__qualname__', sender.__name__))


class CachedBackend(object):

    @staticmethod
    def setup_model(model):
        from .managers import PendingStateLogManager
        model.add_to_class('pending_objects', PendingStateLogManager())

    @staticmethod
    def pre_transition_callback(sender, instance, name, source, target, **kwargs):
        from .models import StateLog

        if BaseBackend._get_model_qualified_name__(sender) in settings.DJANGO_FSM_LOG_IGNORED_MODELS:
            return

        StateLog.pending_objects.create(
            by=getattr(instance, 'by', None),
            state=target,
            transition=name,
            content_object=instance,
        )

    @staticmethod
    def post_transition_callback(sender, instance, name, source, target, **kwargs):
        from .models import StateLog
        StateLog.pending_objects.commit_for_object(instance)


class SimpleBackend(object):

    @staticmethod
    def setup_model(model):
        pass

    @staticmethod
    def pre_transition_callback(sender, **kwargs):
        pass

    @staticmethod
    def post_transition_callback(sender, instance, name, source, target, **kwargs):
        from .models import StateLog

        if BaseBackend._get_model_qualified_name__(sender) in settings.DJANGO_FSM_LOG_IGNORED_MODELS:
            return

        StateLog.objects.create(
            by=getattr(instance, 'by', None),
            state=target,
            transition=name,
            content_object=instance,
        )


if settings.DJANGO_FSM_LOG_STORAGE_METHOD == 'django_fsm_log.backends.CachedBackend':
    try:
        from django.core.cache import caches
    except ImportError:
        from django.core.cache import get_cache  # Deprecated, removed in 1.9.
        cache = get_cache(settings.DJANGO_FSM_LOG_CACHE_BACKEND)
    else:
        cache = caches[settings.DJANGO_FSM_LOG_CACHE_BACKEND]
else:
    cache = None
