from django.contrib import admin

from blog import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin for the Post model.
    """
    autocomplete_fields = ('author',)
    date_hierarchy = 'published'
    fields = ('title', 'author', 'published', 'updated', 'slug', 'content')
    list_display = ('title', 'author', 'published', 'updated')
    readonly_fields = ('slug', 'updated')
    search_fields = ('author__name', 'title')
