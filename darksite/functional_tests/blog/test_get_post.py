import datetime

from django.utils import timezone

from functional_tests import graphql_utils

POST_QUERY = """
query GetPostBySlug($slug: String!) {
  post(slug: $slug) {
    author {
      id
      name
    }
    content
    published
    rendered
    slug
    title
    updated
  }
}
"""


def test_get_post(api_client, post_factory):
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

    response = api_client.query(POST_QUERY, variables={"slug": post.slug})
    response.raise_for_status()

    assert response.status_code == 200
    assert response.json() == {"data": {"post": expected}}


def test_get_post_unpublished(api_client, post_factory):
    """
    Attempting to fetch an unpublished post should behave the same as if
    the post didn't exist.
    """
    now = timezone.now()
    later = now + datetime.timedelta(days=1)
    post = post_factory(published=later)

    response = api_client.query(POST_QUERY, variables={"slug": post.slug})
    response.raise_for_status()

    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(), "Post matching query does not exist.", path=["post"]
    )
