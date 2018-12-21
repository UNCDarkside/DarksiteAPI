from cms import models, schema


class DummyInfo:
    """
    Class to simulate the info passed to the resolver methods.
    """

    def __init__(self, context):
        """
        Initialize the dummy info object.

        Args:
            context:
                The context used during the field resolution.
        """
        self.context = context


def test_resolve_image_no_image():
    """
    If a media resource has no image, the field should resolve to
    ``None``.
    """
    resource = models.MediaResource()

    assert schema.MediaResourceType.resolve_image(resource, None) is None


def test_resolve_image_with_image(image, rf):
    """
    If a media resource has an image, the field should resolve to the
    URL of the media resource's image.
    """
    resource = models.MediaResource(image=image)
    request = rf.get('/')
    info = DummyInfo(request)

    expected = request.build_absolute_uri(resource.image.url)

    assert schema.MediaResourceType.resolve_image(resource, info) == expected


def test_resolve_youtube_id_no_id():
    """
    If the media resource does not have a YouTube video ID, the field
    should resolve to ``None``.
    """
    resource = models.MediaResource()

    assert schema.MediaResourceType.resolve_youtube_id(resource, None) is None


def test_resolve_youtube_id_with_id():
    """
    If the media resource has a YouTube video ID, it should be returned.
    """
    resource = models.MediaResource(youtube_id='dQw4w9WgXcQ')
    result = schema.MediaResourceType.resolve_youtube_id(resource, None)

    assert result == resource.youtube_id
