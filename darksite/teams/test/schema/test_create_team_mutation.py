import pytest

from teams import schema, models


class DummyInfo:
    def __init__(self, context):
        self.context = context


def test_mutate(rf, user_factory):
    """
    If the requesting user is a staff user, a new team should be
    created.
    """
    mutation = schema.CreateTeam()

    user = user_factory(is_staff=True)
    request = rf.post("/")
    request.user = user
    year = 2018

    result = mutation.mutate(DummyInfo(request), year=year)
    team = models.Team.objects.get()

    assert result.team == team


def test_mutate_non_staff(rf, user_factory):
    """
    If the requesting user is not a staff user, an exception should be
    raised.
    """
    mutation = schema.CreateTeam()

    user = user_factory()
    request = rf.post("/")
    request.user = user

    with pytest.raises(Exception):
        mutation.mutate(DummyInfo(request), year=2018)

    assert not models.Team.objects.exists()


def test_mutate_non_unique(rf, team_factory, user_factory):
    """
    Attempting to create a team for a year that already has a team
    should throw an error.
    """
    mutation = schema.CreateTeam()

    user = user_factory(is_staff=True)
    request = rf.post("/")
    request.user = user

    year = 2018
    team_factory(year=year)

    with pytest.raises(Exception):
        mutation.mutate(DummyInfo(request), year=year)

    assert models.Team.objects.count() == 1
