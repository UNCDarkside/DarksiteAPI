import requests


ALBUM_LIST_QUERY = """
query {
  albums {
    created
    description
    slug
    title
  }
}
"""


def test_list_albums(album_factory, live_server):
    """
    Users should be able to list the albums in the system.
    """
    a1 = album_factory(
        description="Album A contains albatross.", title="Album A"
    )
    a2 = album_factory(
        description="Album C contains cool cats.", title="Album C"
    )
    a3 = album_factory(
        description="Album B contains bananas.", title="Album B"
    )

    expected = []
    for album in [a3, a2, a1]:
        expected.append(
            {
                "created": album.created.isoformat(),
                "description": album.description,
                "slug": album.slug,
                "title": album.title,
            }
        )

    response = requests.get(
        f"{live_server.url}/graphql/", json={"query": ALBUM_LIST_QUERY}
    )
    response.raise_for_status()

    assert response.status_code == 200
    assert response.json() == {"data": {"albums": expected}}
