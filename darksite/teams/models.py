import logging

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


class Person(models.Model):
    """
    A person that can be associated with multiple teams.
    """

    created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time the person was created at."),
        verbose_name=_("creation time"),
    )
    name = models.CharField(
        db_index=True,
        help_text=_("The person's name."),
        max_length=100,
        verbose_name=_("name"),
    )
    slug = models.SlugField(
        help_text=_("A unique slug used to identify the person."),
        unique=True,
        verbose_name=_("slug"),
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text=_("The timestamp of the last time the person was updated."),
        verbose_name=_("last update time"),
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def __repr__(self):
        """
        Returns:
            A string representation of the instance that can be used to
            reconstruct it.
        """
        return f"Person(name={repr(self.name)}, slug={repr(self.slug)})"

    def __str__(self):
        """
        Returns:
            A user readable string describing the person.
        """
        return self.name

    def clean(self):
        """
        Generate a slug for the person if they do not have one.
        """
        super().clean()

        if not self.slug:
            # The first choice is simply the slugified version of the
            # person's name.
            slug = slugify(self.name)
            attempt = 1

            # If the first choice is taken, we add an incrementing
            # suffix until the slug is unique.
            while self.__class__.objects.filter(slug=slug).exists():
                attempt += 1
                slug = f"{slugify(self.name)}-{attempt}"

            logger.debug(
                'Generated slug "%s" for person with name "%s"',
                slug,
                self.name,
            )
            self.slug = slug


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
