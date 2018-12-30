import factory

from test_utils import CleanAndSaveFactoryMixin


class PersonFactory(CleanAndSaveFactoryMixin, factory.DjangoModelFactory):
    """
    Factory for generating :class:`.Person` instances for testing.
    """

    name = factory.Sequence(lambda n: f"Person {n}")

    class Meta:
        model = "teams.Person"


class TeamFactory(factory.DjangoModelFactory):
    """
    Factory for generating :class:`.Team` instances for testing.
    """

    year = factory.Sequence(lambda n: n)

    class Meta:
        model = "teams.Team"
