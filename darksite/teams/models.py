from django.db import models
from django.utils.translation import ugettext_lazy as _


class Team(models.Model):
    """
    A team for a specific year.
    """

    created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time the team was created at."),
        verbose_name=_("creation time"),
    )
    year = models.PositiveSmallIntegerField(
        help_text=_("The year that the team had their season."),
        unique=True,
        verbose_name=_("year"),
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text=_("The last time the team was updated."),
        verbose_name=_("last update time"),
    )

    class Meta:
        ordering = ("-year",)
        verbose_name = _("team")
        verbose_name_plural = _("teams")

    def __repr__(self):
        """
        Returns:
            A string containing the information required to reconstruct
            the team.
        """
        return f"Team(year={self.year})"

    def __str__(self):
        """
        Returns:
            A user readable string describing the years the team
            instance played for.
        """
        return f"Darkside {self.year - 1}/{self.year}"
