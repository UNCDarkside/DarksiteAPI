import uuid

import requests

from functional_tests import serializer_utils, graphql_utils


MEDIA_RESOURCE_QUERY = """
query {{
  mediaResource(id: "{id}") {{
    caption
    created
    id
    image
    title
    type
    youtubeId
  }}
}}
"""


def test_get_media_resource(image, live_server, media_resource_factory):
    """
    Users should be able to fetch a media resource by its ID through the
    API.
    """
    resource = media_resource_factory(image=image)
    expected = serializer_utils.serialize_media_resource(
        resource, live_server.url
    )

    response = requests.get(
        f"{live_server.url}/graphql/",
        json={"query": MEDIA_RESOURCE_QUERY.format(id=resource.id)},
    )
    response.raise_for_status()

    assert response.status_code == 200
    assert response.json() == {"data": {"mediaResource": expected}}


def test_get_media_resource_invalid_id(live_server):
    """
    If there is no media resource corresponding to the provided ID, an
    error should be raised.
    """
    response = requests.get(
        f"{live_server.url}/graphql/",
        json={"query": MEDIA_RESOURCE_QUERY.format(id=uuid.uuid4())},
    )
    response.raise_for_status()

    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(),
        "MediaResource matching query does not exist.",
        path=["mediaResource"],
    )
