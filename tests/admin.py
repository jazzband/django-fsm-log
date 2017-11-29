from django.contrib import admin
from django_fsm_log.admin import StateLogInline

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    inlines = [StateLogInline]


admin.site.register(Article, ArticleAdmin)
