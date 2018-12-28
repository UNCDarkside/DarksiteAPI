import requests

from cms.blog import models


POST_LIST_QUERY = """
query {
  posts {
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


def test_list_posts(live_server, post_factory):
    """
    Users should be able to query a list of blog posts through the
    GraphQL API.
    """
    # Assuming there are two posts already in the database...
    post_factory(content="# Post 1", title="Post 1")
    post_factory(content="# Post 2", title="Post 2")

    # I would expect my response to be...
    expected = []
    for post in models.Post.objects.all():
        expected.append(
            {
                "author": {
                    "id": str(post.author.id),
                    "name": post.author.name,
                },
                "content": post.content,
                "published": post.published.isoformat(),
                "rendered": post.rendered,
                "slug": post.slug,
                "title": post.title,
                "updated": post.updated.isoformat(),
            }
        )

    # Make the actual request
    response = requests.get(
        f"{live_server.url}/graphql/", json={"query": POST_LIST_QUERY}
    )
    response.raise_for_status()
    response_data = response.json()

    # Check content
    assert response.status_code == 200
    assert response_data == {"data": {"posts": expected}}
