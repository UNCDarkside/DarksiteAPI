import uuid

import pytest

from cms import schema, models


def test_resolve_album(album_factory):
    """
    Querying for an album by its slug should return the album.
    """
    query = schema.Query()
    album = album_factory()

    assert query.resolve_album(None, slug=album.slug) == album


def test_resolve_albums(album_factory):
    """
    This field should resolve to a list of all albums.
    """
    query = schema.Query()
    album_factory()
    album_factory()

    result = query.resolve_albums(None)

    assert list(result) == list(models.Album.objects.all())


def test_resolve_info_panels(info_panel_factory):
    """
    This field should resolve to a list of all info panels.
    """
    query = schema.Query()
    info_panel_factory()
    info_panel_factory()

    result = query.resolve_info_panels()

    assert list(result) == list(models.InfoPanel.objects.all())


def test_resolve_media_resource(media_resource_factory):
    """
    Querying for a media resource by its id should return the resource.
    """
    query = schema.Query()
    resource = media_resource_factory()

    assert query.resolve_media_resource(None, id=resource.id) == resource


def test_resolve_media_resource_missing(db):
    """
    If the provided ID does not match a media resource, an exception
    should be raised.
    """
    query = schema.Query()

    with pytest.raises(models.MediaResource.DoesNotExist):
        query.resolve_media_resource(uuid.uuid4())
