from django.core.cache import get_cache
from django_fsm_log.conf import settings


class BaseBackend(object):
    def pre_transition_callback(*args, **kwargs):
        raise NotImplementedError

    def post_transition_callback(*args, **kwargs):
        raise NotImplementedError


class CachedBackend(object):

    def __init__(self, *args, **kwargs):
        from django_fsm_log.models import StateLog
        from django_fsm_log.managers import PendingStateLogManager
        self._state_log = StateLog.add_to_class('pending_objects', PendingStateLogManager())

    def pre_transition_callback(sender, instance, name, source, target, **kwargs):
        self._state_log.pending_objects.create(
            by=getattr(instance, 'by', None),
            state=target,
            transition=name,
            content_object=instance,
        )

    def post_transition_callback(sender, instance, name, source, target, **kwargs):
        self._state_log.pending_objects.commit_for_object(instance)


class SimpleBackend(object):

    def __init__(self, *args, **kwargs):
        from django_fsm_log.models import StateLog
        self._state_log = StateLog

    def pre_transition_callback(*args, **kwargs):
        pass

    def post_transition_callback(sender, instance, name, source, target, **kwargs):
        state_log = self._state_log(
            by=getattr(instance, 'by', None),
            state=target,
            transition=name,
            content_object=instance,
        )
        state_log.save()


if settings.DJANGO_FSM_LOG_CACHE_BACKEND:
    cache = get_cache('default')
else:
    cache = None
