from django.contrib import admin

from .models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "created", "expiration", "url")
    list_display_links = ("title",)
