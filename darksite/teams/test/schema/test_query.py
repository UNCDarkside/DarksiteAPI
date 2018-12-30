from teams import schema, models


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
