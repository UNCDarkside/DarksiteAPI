from teams import models


def test_ordering(team_factory):
    """
    Teams should be ordered by year, descending.
    """
    t1 = team_factory(year=2018)
    t2 = team_factory(year=2019)
    t3 = team_factory(year=2017)

    assert list(models.Team.objects.all()) == [t2, t1, t3]


def test_repr():
    """
    The string representation of a team should include the information
    needed to reconstruct the team.
    """
    team = models.Team(year=2018)
    expected = f"Team(year={repr(team.year)})"

    assert repr(team) == expected


def test_str():
    """
    Converting a team to a string should return a string stating the
    year range that the team played.
    """
    team = models.Team(year=2018)
    expected = f"Darkside {team.year - 1}/{team.year}"

    assert str(team) == expected
