TEAM_LIST_QUERY = """
query ListTeams {
  teams {
    year
  }
}
"""


def test_list_teams(api_client, team_factory):
    """
    Any user should be able to list the teams in the system. The result
    should be ordered by year, descending.
    """
    # Given the following teams in the database...
    t1 = team_factory(year=2018)
    t2 = team_factory(year=2019)
    t3 = team_factory(year=2017)

    # June, a user of the site, requests a list of all teams.
    response = api_client.query(TEAM_LIST_QUERY)

    # She receives a response containing the teams listed in order of
    # year, descending.
    assert response.status_code == 200, response.content
    assert response.json() == {
        "data": {
            "teams": list(map(lambda team: {"year": team.year}, [t2, t1, t3]))
        }
    }
