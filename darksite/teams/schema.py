import logging

import graphene
import graphene_django
from django.utils.translation import ugettext_lazy as _, ugettext
from graphql import GraphQLError

from teams import models


logger = logging.getLogger(__name__)


class PersonType(graphene_django.DjangoObjectType):
    """
    A person who can be associated with teams for different years.
    """

    class Meta:
        only_fields = ("name", "slug")
        model = models.Person


class TeamType(graphene_django.DjangoObjectType):
    """
    A team for a specific year.
    """

    class Meta:
        only_fields = ("year",)
        model = models.Team


class CreatePerson(graphene.Mutation):
    """
    Mutation to create a new person.
    """

    person = graphene.Field(
        PersonType, description=_("The newly created person.")
    )

    class Arguments:
        name = graphene.String(
            description=_("The name of the person to create."), required=True
        )

    def mutate(self, info, name):
        """
        Create a new person.

        Only staff users are permitted to execute this mutation.

        Args:
            info:
                Information about the request being made.
            name:
                The name of the person to create.

        Returns:
            An object containing the created person.
        """
        if not info.context.user.is_staff:
            raise GraphQLError(
                ugettext("You do not have permission to create a new person.")
            )

        person = models.Person(name=name)
        person.clean()
        person.save()

        return CreatePerson(person=person)


class CreateTeam(graphene.Mutation):
    """
    Mutation to create a new team for a specific year.
    """

    team = graphene.Field(TeamType, description=_("The newly created team."))

    class Arguments:
        year = graphene.Int(
            description=_("The year that the team had their regular season."),
            required=True,
        )

    def mutate(self, info, year):
        """
        Create a new team.

        Args:
            info:
                Information about the request being made.
            year:
                The year to create the team for.

        Returns:
            An object containing the created team.
        """
        if not info.context.user.is_staff:
            logger.info(
                "Denied non-staff user from creating a team: %r",
                info.context.user,
            )
            raise Exception(
                ugettext("You do not have permission to create a team.")
            )

        if models.Team.objects.filter(year=year).exists():
            logger.info(
                "Prohibited creation of a duplicate team for the year %d.",
                year,
            )
            raise Exception(
                ugettext(
                    "There is already a team for the year {year}."
                ).format(year=year)
            )

        team = models.Team.objects.create(year=year)
        logger.info("Created team %r", team)

        return CreateTeam(team=team)


class Mutations(graphene.ObjectType):
    create_person = CreatePerson.Field(
        description=_(
            "Create a new person. People can then be associated with "
            "specific teams."
        )
    )
    create_team = CreateTeam.Field(
        description=_(
            "Create a new team for a specific year. Only staff users are "
            "allowed to create a new team."
        )
    )
