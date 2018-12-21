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
    # We have to redefine the field so it can be null.
    image = graphene.String(
        description=_(
            "The URL of the image that the media resource points to."
        ),
    )
    type = graphene.String(
        description=_(
            'A string describing the type of media that the object '
            'encapsulates.'
        )
    )
    # We have to redefine the field so it can be null.
    youtube_id = graphene.String(
        description=_(
            "The ID of the YouTube video that the media resource points to."
        ),
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
        """
        Resolve the media resource's image.

        Args:
            instance:
                The instance to resolve the image of.
            info:
                Additional information used to resolve the request.

        Returns:
            The full URI of the resource's image if it has one and
            ``None`` if it doesn't.
        """
        if not instance.image:
            return None

        return info.context.build_absolute_uri(instance.image.url)

    @staticmethod
    def resolve_youtube_id(instance, *args, **kwargs):
        """
        Resolve the media resource's YouTube video ID.

        Args:
            instance:
                The instance to resolve the YouTube video ID of.

        Returns:
            The ID of the resources YouTube video if it has one and
            ``None`` otherwise.
        """
        if not instance.youtube_id:
            return None

        return instance.youtube_id


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

    @staticmethod
    def resolve_info_panels(*args, **kwargs):
        """
        Returns:
            All info panels in the database.
        """
        return models.InfoPanel.objects.all()

    @staticmethod
    def resolve_media_resource(*args, id=None, **kwargs):
        """
        Returns:
            Returns the media resource with the specified ID.
        """
        return models.MediaResource.objects.get(id=id)
