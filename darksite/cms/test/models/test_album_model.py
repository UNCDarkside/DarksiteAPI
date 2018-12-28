from django.utils.text import slugify

from cms import models


def test_clean_existing_slug():
    """
    If an album has a slug, cleaning it should not change the slug.
    """
    slug = "my-slug"
    album = models.Album(slug=slug, title="Random Title")

    album.clean()

    assert album.slug == slug


def test_clean_no_slug():
    """
    If an album does not have a slug, cleaning it should generate one
    from the album's title.
    """
    title = "My Title"
    album = models.Album(title=title)

    album.clean()

    assert album.slug.startswith(slugify(title))


def test_ordering(album_factory):
    """
    Albums should be ordered by creation time, descending.
    """
    a1 = album_factory(title="A")
    a2 = album_factory(title="C")
    a3 = album_factory(title="B")

    assert list(models.Album.objects.all()) == [a3, a2, a1]


def test_repr():
    """
    The string representation of an album should contain the information
    required to reconstruct it.
    """
    album = models.Album(title="Test Album")
    expected = (
        f"Album(created={repr(album.created)}, slug={repr(album.slug)}, "
        f"title={repr(album.title)})"
    )

    assert repr(album) == expected


def test_str():
    """
    The string representation of an album should be its title.
    """
    album = models.Album(title="Test Album")

    assert str(album) == album.title
