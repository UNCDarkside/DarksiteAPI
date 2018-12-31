from django.contrib import admin

from teams import models


class TeamMemberInline(admin.TabularInline):
    """
    Inline for managing team members.
    """

    autocomplete_fields = ("person",)
    fields = ("person", "team", "role", "number")
    model = models.TeamMember


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    """
    Admin for the :class:`Person` model.
    """

    date_hierarchy = "created"
    fields = ("name", "slug", "created", "updated")
    inlines = (TeamMemberInline,)
    list_display = ("name", "slug", "created", "updated")
    readonly_fields = ("slug", "created", "updated")
    search_fields = ("name", "slug")


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin for the :class:`Team` model.
    """

    fields = ("year", "created", "updated")
    inlines = (TeamMemberInline,)
    list_display = ("name", "created", "updated")
    readonly_fields = ("created", "updated")
    search_fields = ("year",)

    def name(self, instance):
        return str(instance)

    name.admin_order_field = "year"


@admin.register(models.TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """
    Admin for the :class:`TeamMember` model.
    """

    autocomplete_fields = ("person", "team")
    fields = ("person", "team", "role", "number", "created", "updated")
    list_display = ("person", "team", "role", "number")
    list_filter = ("role",)
    readonly_fields = ("created", "updated")
    search_fields = ("number", "person__name", "team__year")
