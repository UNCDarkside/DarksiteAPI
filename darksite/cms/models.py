import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext


def get_media_resource_image_path(_, file):
    """
    Get the path that a media resource's image should be uploaded to.

    Args:
        _:
            The media resource the image belongs to.
        file:
            The original name of the file being uploaded.

    Returns:
        The path that the media resource should be uploaded to.
    """
    return f'cms/media-resources/images/{file}'


class InfoPanel(models.Model):
    """
    A panel containing information about the team.
    """
    id = models.UUIDField(
        default=uuid.uuid4,
        help_text=_('A unique identifier for the panel.'),
        primary_key=True,
        verbose_name=_('ID'),
    )
    media = models.ForeignKey(
        'cms.MediaResource',
        blank=True,
        help_text=_('The media to show in the panel.'),
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('media resource'),
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text=_(
            'An integer describing position of the panel in relation to '
            'other panels.'
        ),
        verbose_name=_('order'),
    )
    text = models.TextField(
        help_text=_('The text to display in the panel.'),
        verbose_name=_('text'),
    )
    title = models.CharField(
        help_text=_('The title of the panel.'),
        max_length=100,
        verbose_name=_('title'),
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _('info panel')
        verbose_name_plural = _('info panels')

    def __repr__(self):
        """
        Returns:
            A string containing the information required to reconstruct
            the instance.
        """
        return f'InfoPanel(id={repr(self.id)}, title={repr(self.title)})'

    def __str__(self):
        """
        Returns:
            A user readable string describing the instance.
        """
        return self.title


class MediaResource(models.Model):
    """
    A container for a single media object such as an image or video.
    """
    TYPE_IMAGE = 'image'
    TYPE_YOUTUBE = 'youtube'

    caption = models.TextField(
        blank=True,
        help_text=_('A caption for the resource.'),
        verbose_name=_('caption'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time that the resource was created at.'),
        verbose_name=_('creation time'),
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        help_text=_('A unique identifier for the media resource.'),
        primary_key=True,
        verbose_name=_('ID'),
    )
    is_listed = models.BooleanField(
        default=True,
        help_text=_(
            'Designates if the resource is listed publicly. Unlisted images '
            'can still be accessed by anyone with the ID of the resource.'
        ),
        verbose_name=_('listed'),
    )
    image = models.ImageField(
        blank=True,
        help_text=_('The image that the media resource encapsulates.'),
        upload_to=get_media_resource_image_path,
        verbose_name=_('image'),
    )
    title = models.CharField(
        blank=True,
        help_text=_('A title for the resource.'),
        max_length=100,
        verbose_name=_('title'),
    )
    youtube_id = models.CharField(
        blank=True,
        help_text=_('The ID of the YouTube video the resource encapsulates.'),
        max_length=32,
        verbose_name=_('YouTube ID'),
    )

    class Meta:
        ordering = ('created',)
        verbose_name = _('media resource')
        verbose_name_plural = _('media resources')

    def __str__(self):
        """
        Returns:
            A user readable string describing the instance.
        """
        ret_str = str(self.id)

        if self.title:
            ret_str += f' ({self.title})'

        return ret_str

    def clean(self):
        """
        Ensure that the resource contains exactly one type of media.
        """
        super().clean()

        if self.image and self.youtube_id:
            raise ValidationError(
                ugettext(
                    'A media resource may not contain both an image and a '
                    'YouTube video.'
                )
            )

        if not self.image and not self.youtube_id:
            raise ValidationError(
                ugettext(
                    'A media resource must contain an image or YouTube video.'
                )
            )

    @property
    def type(self):
        """
        Returns:
            The type of the resource.
        """
        if self.image:
            return self.TYPE_IMAGE

        return self.TYPE_YOUTUBE
