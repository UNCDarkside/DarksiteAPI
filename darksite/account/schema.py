from django.utils.translation import ugettext_lazy as _
import graphene
import graphene_django

from account import models


class UserType(graphene_django.DjangoObjectType):
    """
    A user of the site.
    """
    class Meta:
        only_fields = ('id', 'name')
        model = models.User


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
