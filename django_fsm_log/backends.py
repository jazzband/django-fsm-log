from django.core.cache import get_cache
from django_fsm_log.conf import settings


class BaseBackend(object):
    def pre_transition_callback(*args, **kwargs):
        raise NotImplementedError

    def post_transition_callback(*args, **kwargs):
        raise NotImplementedError


class CachedBackend(object):

    @staticmethod
    def pre_transition_callback(sender, instance, name, source, target, **kwargs):
        from django_fsm_log.models import StateLog
        StateLog.pending_objects.create(
            by=getattr(instance, 'by', None),
            state=target,
            transition=name,
            content_object=instance,
        )

    @staticmethod
    def post_transition_callback(sender, instance, name, source, target, **kwargs):
        from django_fsm_log.models import StateLog
        StateLog.pending_objects.commit_for_object(instance)


class SimpleBackend(object):

    @staticmethod
    def pre_transition_callback(sender, **kwargs):
        pass

    @staticmethod
    def post_transition_callback(sender, instance, name, source, target, **kwargs):
        from django_fsm_log.models import StateLog
        log = StateLog.objects.create(
            by=getattr(instance, 'by', None),
            state=target,
            transition=name,
            content_object=instance,
        )
        log.save()


if settings.DJANGO_FSM_LOG_CACHE_BACKEND:
    cache = get_cache('default')
else:
    cache = None
