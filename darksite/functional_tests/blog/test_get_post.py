import datetime

import requests


# Note braces are doubled to allow formatting.
from django.utils import timezone

from functional_tests import graphql_utils

POST_QUERY = """
query {{
  post(slug: "{slug}") {{
    author {{
      id
      name
    }}
    content
    published
    rendered
    slug
    title
    updated
  }}
}}
"""


def test_get_post(live_server, post_factory):
    """
    Users should be able to query for a published post by its slug.
    """
    post = post_factory(
        content="A post that should be fetch-able.", title="Published Post"
    )
    expected = {
        "author": {"id": str(post.author.id), "name": post.author.name},
        "content": post.content,
        "published": post.published.isoformat(),
        "rendered": post.rendered,
        "slug": post.slug,
        "title": post.title,
        "updated": post.updated.isoformat(),
    }

    response = requests.get(
        f"{live_server.url}/graphql/",
        json={"query": POST_QUERY.format(slug=post.slug)},
    )
    response.raise_for_status()

    assert response.status_code == 200
    assert response.json() == {"data": {"post": expected}}


def test_get_post_unpublished(live_server, post_factory):
    """
    Attempting to fetch an unpublished post should behave the same as if
    the post didn't exist.
    """
    now = timezone.now()
    later = now + datetime.timedelta(days=1)
    post = post_factory(published=later)

    response = requests.get(
        f"{live_server.url}/graphql/",
        json={"query": POST_QUERY.format(slug=post.slug)},
    )
    response.raise_for_status()
    response_data = response.json()

    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response_data, "Post matching query does not exist.", path=["post"]
    )
