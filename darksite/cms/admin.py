from django.contrib import admin

from cms import models


@admin.register(models.MediaResource)
class MediaResourceAdmin(admin.ModelAdmin):
    """
    Admin for media resources.
    """
    date_hierarchy = 'created'
    fields = (
        'image',
        'youtube_id',
        'created',
        'title',
        'is_listed',
        'caption',
    )
    list_display = ('title', 'id', 'is_listed')
    list_filter = ('is_listed',)
    readonly_fields = ('created',)
    search_fields = ('caption', 'id', 'title', 'youtube_id')
