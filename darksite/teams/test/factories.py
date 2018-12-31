import factory

from teams import models
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


class TeamMemberFactory(factory.DjangoModelFactory):
    """
    Factory for generating :class:`TeamMember` instances for testing.
    """

    number = factory.Sequence(int)
    person = factory.SubFactory("teams.test.factories.PersonFactory")
    role = models.TeamMember.PLAYER
    team = factory.SubFactory("teams.test.factories.TeamFactory")

    class Meta:
        model = "teams.TeamMember"
