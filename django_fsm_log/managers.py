import django
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django_fsm_log.backends import cache


class StateLogQuerySet(QuerySet):
    def _get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj)

    def for_(self, obj):
        return self.filter(
            content_type=self._get_content_type(obj),
            object_id=obj.pk
        )


class StateLogManager(models.Manager):
    def get_queryset(self):
        return StateLogQuerySet(self.model)

    if django.VERSION < (1, 7):
        get_query_set = get_queryset

    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_queryset(), attr, *args)


class PendingStateLogManager(models.Manager):
    def _get_cache_key_for_object(self, obj):
        return 'StateLog:{}:{}'.format(
            obj.__class__.__name__,
            obj.pk
        )

    def create(self, *args, **kwargs):
        log = self.model(**kwargs)
        key = self._get_cache_key_for_object(kwargs['content_object'])
        cache.set(key, log, 10)
        return log

    def commit_for_object(self, obj):
        key = self._get_cache_key_for_object(obj)
        log = self.get_for_object(obj)
        log.save()
        cache.delete(key)
        return log

    def get_for_object(self, obj):
        key = self._get_cache_key_for_object(obj)
        return cache.get(key)
