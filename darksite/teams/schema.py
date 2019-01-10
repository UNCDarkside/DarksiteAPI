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


class TeamMemberType(graphene_django.DjangoObjectType):
    """
    An association between a person and a team. This association
    contains additional information such as the person's role on the
    team or their number if they are a player.
    """

    class Meta:
        only_fields = ("number", "person", "role", "team")
        model = models.TeamMember


class TeamType(graphene_django.DjangoObjectType):
    """
    A team for a specific year.
    """

    class Meta:
        only_fields = ("year",)
        model = models.Team


class AddTeamMember(graphene.Mutation):
    """
    Add a person to a team. This association contains information such
    as the member's role on the team or their number.
    """

    team_member = graphene.Field(
        TeamMemberType,
        description=_("The newly created team member."),
        required=True,
    )

    class Arguments:
        number = graphene.Int(
            description=_("The team member's number if they are a player.")
        )
        person_slug = graphene.String(
            description=_("The slug of the person to add as a team member."),
            required=True,
        )
        role = graphene.String(
            description=_("The role of the team member to add."), required=True
        )
        team_year = graphene.Int(
            description=_("The year of the team to add the member to."),
            required=True,
        )

    def mutate(self, info, person_slug, role, team_year, number=None):
        """
        Create a new team member associating a person with a team.

        Args:
            info:
                An object containing information about the request being
                made.
            person_slug:
                The slug of the person to associate with the new team
                member.
            role:
                The role to assign to the created team member.
            team_year:
                The year of the team to associate with the new team
                member.
            number:
                The new team member's number, if they are a player.
                Defaults to ``None``.

        Returns:
            An object containing the created team member.
        """
        if not info.context.user.is_staff:
            raise GraphQLError(
                ugettext("You do not have permission to add a team member.")
            )

        try:
            person = models.Person.objects.get(slug=person_slug)
        except models.Person.DoesNotExist:
            raise GraphQLError(
                ugettext(
                    'The person with the slug "{person_slug}" does not exist.'
                ).format(person_slug=person_slug)
            )

        try:
            team = models.Team.objects.get(year=team_year)
        except models.Team.DoesNotExist:
            raise GraphQLError(
                ugettext(
                    "The team for the year {year} does not exist."
                ).format(year=team_year)
            )

        if models.TeamMember.objects.filter(person=person, team=team).exists():
            raise GraphQLError(
                ugettext(
                    "{person} is already a member of the {year} team."
                ).format(person=person.name, year=team.year)
            )

        team_member = models.TeamMember.objects.create(
            number=number, person=person, role=role, team=team
        )
        logger.info(
            "User %s created team member %r",
            info.context.user.email,
            team_member,
        )

        return AddTeamMember(team_member=team_member)


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
    add_team_member = AddTeamMember.Field(
        description=_(
            "Add a person to a team. This association also contains "
            "information such as the team member's role and number."
        )
    )
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


class Query(graphene.ObjectType):
    teams = graphene.List(
        TeamType,
        description=_("List all the teams in the database."),
        required=True,
    )

    @staticmethod
    def resolve_teams(*_):
        """
        Get a list of all teams in the database.

        Returns:
            A queryset containing all the teams in the database ordered
            by year, descending.
        """
        return models.Team.objects.order_by("-year")
