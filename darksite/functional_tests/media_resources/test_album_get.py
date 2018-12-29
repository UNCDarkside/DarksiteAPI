from functional_tests import serializer_utils


ALBUM_QUERY = """
query GetAlbumBySlug($slug: String!) {
  album(slug: $slug) {
    created
    description
    mediaResources {
      caption
      created
      id
      image
      title
      type
      youtubeId
    }
    slug
    title
  }
}
"""


def test_get_album(
    album_factory, api_client, live_server, media_resource_factory
):
    """
    Users should be able to query for a specific album by its slug.
    """
    resource = media_resource_factory(youtube_id="dQw4w9WgXcQ")
    album = album_factory()
    album.media_resources.add(resource)

    expected = {
        "created": album.created.isoformat(),
        "description": album.description,
        "mediaResources": list(
            map(
                lambda media: serializer_utils.serialize_media_resource(
                    media, live_server.url
                ),
                [resource],
            )
        ),
        "slug": album.slug,
        "title": album.title,
    }

    response = api_client.query(ALBUM_QUERY, variables={"slug": album.slug})
    response.raise_for_status()

    assert response.status_code == 200
    assert response.json() == {"data": {"album": expected}}
