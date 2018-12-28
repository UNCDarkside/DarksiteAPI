import datetime
from unittest import mock

import pytest
from django.utils import timezone

from cms.blog import schema, models


def test_resolve_post(post_factory):
    """
    An individual post should be resolveable by its slug.
    """
    query = schema.Query()
    post = post_factory()

    assert query.resolve_post(None, slug=post.slug) == post


def test_resolve_post_invalid_slug(db):
    """
    If a slug has no corresponding post, the resolver should raise an
    exception.
    """
    query = schema.Query()

    with pytest.raises(models.Post.DoesNotExist):
        query.resolve_post(None, slug="does-not-exist")


def test_resolve_post_not_published(post_factory):
    """
    Attempting to resolve a post whose publish time has not arrived
    should act the same as a post that doesn't exist.
    """
    query = schema.Query()

    now = timezone.now()
    later = now + datetime.timedelta(hours=1)
    post = post_factory(published=later)

    with mock.patch(
        "cms.blog.schema.timezone.now", autospec=True, return_value=now
    ):
        with pytest.raises(models.Post.DoesNotExist):
            query.resolve_post(None, slug=post.slug)


def test_resolve_posts(post_factory):
    """
    The posts resolver should return all published posts.
    """
    query = schema.Query()
    now = timezone.now()
    later = now + datetime.timedelta(hours=1)

    post = post_factory(published=now)
    post_factory(published=later)

    with mock.patch(
        "cms.blog.schema.timezone.now", autospec=True, return_value=now
    ):
        result = query.resolve_posts(None)

    assert list(result) == [post]
