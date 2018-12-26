import logging

from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _, ugettext
import graphene
import graphene_django

from account import models


logger = logging.getLogger(__name__)


class UserType(graphene_django.DjangoObjectType):
    """
    A user of the site.
    """
    class Meta:
        only_fields = ('id', 'name')
        model = models.User


class LogIn(graphene.Mutation):
    """
    Mutation to log in.
    """
    user = graphene.Field(type=UserType)

    class Arguments:
        email = graphene.String(
            description=_('The email address of the user to log in as.'),
        )
        password = graphene.String(description=_('The password of the user.'))

    def mutate(self, info, email=None, password=None):
        """
        Log in the user with the provided credentials.

        Args:
            info:
                Object containing information about the request.
            email:
                The email address of the user to log in as.
            password:
                The user's password.
        """
        user = authenticate(password=password, username=email)
        if user is None:
            raise Exception(
                ugettext(
                    "No user with the provided email/password was found."
                )
            )

        login(info.context, user)
        logger.info('Logged in %r', user)

        return LogIn(user=user)


class Mutations(graphene.ObjectType):
    log_in = LogIn.Field(description=_('Log in as a user.'))


class Query(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        id=graphene.UUID(
            description=_('A unique identifier for the user.')
        ),
    )

    @staticmethod
    def resolve_user(*_, id=None, **kwargs):
        """
        Query for a specific user.

        Args:
            id:
                The ID of the user to fetch.

        Returns:
            The user with the provided ID.
        """
        return models.User.objects.get(id=id)
