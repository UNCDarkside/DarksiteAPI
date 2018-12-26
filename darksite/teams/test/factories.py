import factory


class TeamFactory(factory.DjangoModelFactory):
    """
    Factory for generating :class:`.Team` instances for testing.
    """
    year = factory.Sequence(lambda n: n)

    class Meta:
        model = 'teams.Team'
