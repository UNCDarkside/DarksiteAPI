from teams import schema, models


def test_resolve_team(team_factory):
    """
    The team field should resolve to the team with the specified year if
    it exists.
    """
    query = schema.Query()
    team = team_factory()

    assert query.resolve_team(None, year=team.year) == team


def test_resolve_teams(team_factory):
    """
    The teams field should resolve to a list of all teams in order of
    year, descending.
    """
    query = schema.Query()
    team_factory()
    team_factory()

    result = query.resolve_teams(None)

    assert result.query.order_by == ("-year",)
    assert list(result) == list(models.Team.objects.all())
