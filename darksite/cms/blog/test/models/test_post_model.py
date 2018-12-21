from unittest import mock

from django.utils.text import slugify

from cms.blog import models


def test_clean_no_slug():
    """
    If the post does not have a slug, one should be generated. The
    generated slug should begin with the slugified version of the post's
    title.
    """
    title = 'Post Title'
    post = models.Post(title=title)

    post.clean()

    assert post.slug.startswith(slugify(title))


def test_clean_with_slug():
    """
    If the post already has a slug, cleaning it should not change the
    slug.
    """
    slug = 'random-slug'
    post = models.Post(slug=slug, title='Random Title')

    post.clean()

    assert post.slug == slug


@mock.patch(
    'cms.blog.models.markdown.markdown',
    autospec=True,
)
def test_rendered(mock_markdown):
    """
    The ``rendered`` property should return the HTML version of the
    post's Markdown content.
    """
    post = models.Post(content='# Foo')

    content = post.rendered

    assert content == mock_markdown.return_value
    assert mock_markdown.call_args[0] == (post.content,)
    assert mock_markdown.call_args[1] == {
        'output_format': 'html5',
    }


def test_repr(post_factory):
    """
    The representation of a post should include the information required
    to reconstruct it.
    """
    post = post_factory()
    expected = (
        f'Post(author_id={repr(post.author.id)}, slug={repr(post.slug)})'
    )

    assert repr(post) == expected


def test_str():
    """
    Converting a post to a string should return the post's title.
    """
    post = models.Post(title='Test Post')

    assert str(post) == post.title
