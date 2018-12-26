from django.contrib import admin

from teams import models


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin for the :class:`Team` model.
    """
    fields = ('year', 'created', 'updated')
    list_display = ('name', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    search_fields = ('year',)

    def name(self, instance):
        return str(instance)
    name.admin_order_field = 'year'
