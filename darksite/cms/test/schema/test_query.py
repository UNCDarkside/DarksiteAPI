import uuid

import pytest

from cms import schema, models


def test_resolve_media_resource(media_resource_factory):
    """
    Querying for a media resource by its id should return the resource.
    """
    resource = media_resource_factory()
    query = schema.Query()

    assert query.resolve_media_resource(None, id=resource.id) == resource


def test_resolve_media_resource_missing(db):
    """
    If the provided ID does not match a media resource, an exception
    should be raised.
    """
    query = schema.Query()

    with pytest.raises(models.MediaResource.DoesNotExist):
        query.resolve_media_resource(uuid.uuid4())
