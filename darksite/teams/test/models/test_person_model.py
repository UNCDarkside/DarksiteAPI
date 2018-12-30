from django.utils.text import slugify

from teams import models


def test_clean_existing_slug():
    """
    If a person has a slug, cleaning the instance should not change the
    slug.
    """
    slug = "my-slug"
    person = models.Person(name="Jane Smith", slug=slug)

    person.clean()

    assert person.slug == slug


def test_clean_no_slug(db):
    """
    If a person doesn't have a slug, cleaning the instance should
    generate a new slug.
    """
    person = models.Person(name="John Smith")

    person.clean()

    assert person.slug == slugify(person.name)


def test_clean_no_slug_duplicate_name(person_factory):
    """
    If the person doesn't have a slug and there is already a person with
    the same slug, a suffix should be appended to the new person's slug.
    """
    first_person = person_factory()
    second_person = models.Person(name=first_person.name)

    second_person.clean()

    assert second_person.slug == f"{slugify(second_person.name)}-2"


def test_ordering(person_factory):
    """
    People should be ordered by name.
    """
    p1 = person_factory(name="Anna Archer")
    p2 = person_factory(name="Charlie Church")
    p3 = person_factory(name="Billy Boxer")

    assert list(models.Person.objects.all()) == [p1, p3, p2]


def test_repr():
    """
    The representation of a person instance should include the
    information required to reconstruct the person.
    """
    person = models.Person(name="Jane Smith", slug="jane-smith")
    expected = f"Person(name={repr(person.name)}, slug={repr(person.slug)})"

    assert repr(person) == expected


def test_str():
    """
    Converting a person to a string should return the person's name.
    """
    person = models.Person(name="John Smith")

    assert str(person) == person.name
