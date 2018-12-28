import pytest
from django.core.exceptions import ValidationError

from cms import models


def test_str_no_title(media_resource_factory):
    """
    If a resource has no title, it's ID should be returned.
    """
    resource = media_resource_factory()

    assert str(resource) == str(resource.id)


def test_str_with_title(media_resource_factory):
    """
    If a resource has a title, it should be included in the string
    representation.
    """
    resource = media_resource_factory(title="Test Resource")

    assert str(resource) == f"{resource.id} ({resource.title})"


def test_ordering(media_resource_factory):
    """
    Media resources should be ordered by creation time, ascending.
    """
    m1 = media_resource_factory()
    m2 = media_resource_factory()

    assert list(models.MediaResource.objects.all()) == [m1, m2]


def test_clean_both_image_and_youtube_id(image):
    """
    If a media resource has both an image and YouTube video ID specified
    then cleaning it should throw an error.
    """
    resource = models.MediaResource(image=image, youtube_id="dQw4w9WgXcQ")

    with pytest.raises(ValidationError):
        resource.clean()


def test_clean_no_image_or_youtube_id():
    """
    If a media resource does not encapsulate any media, cleaning it
    should throw an error.
    """
    resource = models.MediaResource()

    with pytest.raises(ValidationError):
        resource.clean()


def test_clean_only_image(image):
    """
    Cleaning a media resource that only has an image should do nothing.
    """
    resource = models.MediaResource(image=image)

    resource.clean()


def test_clean_only_youtube_id():
    """
    Cleaning a media resource that only has a YouTube video ID should do
    nothing.
    """
    resource = models.MediaResource(youtube_id="dQw4w9WgXcQ")

    resource.clean()


def test_type_image(image):
    """
    If a media resource has an image, its type property should indicate
    it's an image.
    """
    resource = models.MediaResource(image=image)

    assert resource.type == models.MediaResource.TYPE_IMAGE


def test_type_youtube():
    """
    If a media resource has a YouTube video ID, its type property should
    indicate it's a YouTube video.
    """
    resource = models.MediaResource(youtube_id="dQw4w9WgXcQ")

    assert resource.type == models.MediaResource.TYPE_YOUTUBE
