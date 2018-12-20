import graphene_django
from django.utils.translation import ugettext_lazy as _
import graphene

from cms import models


class InfoPanelType(graphene_django.DjangoObjectType):
    """
    A panel with a heading, text, and a media resource.
    """

    class Meta:
        only_fields = (
            'id',
            'media',
            'text',
            'title',
        )
        model = models.InfoPanel


class MediaResourceType(graphene_django.DjangoObjectType):
    """
    A media object with some additional descriptive information.
    """
    type = graphene.String(
        description=_(
            'A string describing the type of media that the object '
            'encapsulates.'
        )
    )

    class Meta:
        only_fields = (
            'caption',
            'created',
            'id',
            'is_listed',
            'image',
            'title',
            'type',
            'youtube_id',
        )
        model = models.MediaResource

    @staticmethod
    def resolve_image(instance, info):
        if not instance.image:
            return None

        return info.context.build_absolute_uri(instance.image.url)


class Query(graphene.ObjectType):
    info_panels = graphene.List(
        InfoPanelType,
        description=_('Get a list of all information panels.'),
    )
    media_resource = graphene.Field(
        MediaResourceType,
        description=_('Get a specific media resource.'),
        id=graphene.UUID(
            description=_('The ID of a media resource.')
        )
    )

    def resolve_info_panels(self, info, **kwargs):
        """
        Returns:
            All info panels in the database.
        """
        return models.InfoPanel.objects.all()

    def resolve_media_resource(self, info, id=None, **kwargs):
        """
        Returns:
            Returns the media resource with the specified ID.
        """
        return models.MediaResource.objects.get(id=id)
