from django.contrib import admin

from teams import models


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    """
    Admin for the :class:`Person` model.
    """

    date_hierarchy = "created"
    fields = ("name", "slug", "created", "updated")
    list_display = ("name", "slug", "created", "updated")
    readonly_fields = ("slug", "created", "updated")
    search_fields = ("name", "slug")


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin for the :class:`Team` model.
    """

    fields = ("year", "created", "updated")
    list_display = ("name", "created", "updated")
    readonly_fields = ("created", "updated")
    search_fields = ("year",)

    def name(self, instance):
        return str(instance)

    name.admin_order_field = "year"
