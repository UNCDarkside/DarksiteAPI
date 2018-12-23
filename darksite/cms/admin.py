from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from cms import models


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    """
    Admin for albums of media resources.
    """
    date_hierarchy = 'created'
    fields = ('title', 'slug', 'description', 'media_resources')
    filter_horizontal = ('media_resources',)
    list_display = ('title', 'created')
    readonly_fields = ('slug',)
    search_fields = ('title',)


@admin.register(models.InfoPanel)
class InfoPanelAdmin(SortableAdminMixin, admin.ModelAdmin):
    """
    Admin for info panels.
    """
    fields = ('title', 'text', 'media')
    list_display = ('order', 'title')
    list_display_links = ('title',)
    search_fields = ('title',)


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
