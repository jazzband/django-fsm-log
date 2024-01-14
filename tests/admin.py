from django.contrib import admin

from django_fsm_log.admin import PersistedTransitionInline

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [PersistedTransitionInline]
