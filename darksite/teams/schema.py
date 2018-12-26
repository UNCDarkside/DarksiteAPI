import logging

import graphene
import graphene_django
from django.utils.translation import ugettext_lazy as _, ugettext

from teams import models


logger = logging.getLogger(__name__)


class TeamType(graphene_django.DjangoObjectType):
    """
    A team for a specific year.
    """

    class Meta:
        only_fields = ('year',)
        model = models.Team


class CreateTeam(graphene.Mutation):
    """
    Mutation to create a new team for a specific year.
    """
    team = graphene.Field(
        TeamType,
        description=_('The newly created team.'),
    )

    class Arguments:
        year = graphene.Int(
            description=_('The year that the team had their regular season.'),
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
                'Denied non-staff user from creating a team: %r',
                info.context.user,
            )
            raise Exception(
                ugettext("You do not have permission to create a team."),
            )

        if models.Team.objects.filter(year=year).exists():
            logger.info(
                'Prohibited creation of a duplicate team for the year %d.',
                year,
            )
            raise Exception(
                ugettext(
                    "There is already a team for the year {year}."
                ).format(year=year)
            )

        team = models.Team.objects.create(year=year)
        logger.info('Created team %r', team)

        return CreateTeam(team=team)


class Mutations(graphene.ObjectType):
    create_team = CreateTeam.Field(
        description=_(
            'Create a new team for a specific year. Only staff users are '
            'allowed to create a new team.'
        ),
    )
