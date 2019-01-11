from functional_tests import graphql_utils

TEAM_QUERY = """
query GetTeamForYear($year: Int!) {
  team(year: $year) {
    members {
      number
      person {
        name
        slug
      }
      role
    }
  }
}
"""


def test_get_team(api_client, team_factory, team_member_factory):
    """
    Users should be able to fetch a team for a specific year.
    """
    # Given an existing team with members...
    team = team_factory()
    team_member_factory(number=None, role="C", team=team)
    team_member_factory(number=None, role="C", team=team)
    team_member_factory(number=42, role="P", team=team)
    team_member_factory(number=12, role="P", team=team)

    # Any user should be able to retrieve the team by its year.
    response = api_client.query(TEAM_QUERY, variables={"year": team.year})

    # The response should contain the team information along with its
    # members.
    expected = {
        "members": list(
            map(
                lambda member: {
                    "number": member.number,
                    "person": {
                        "name": member.person.name,
                        "slug": member.person.slug,
                    },
                    "role": member.role,
                },
                team.teammember_set.all(),
            )
        )
    }

    assert response.status_code == 200, response.content
    assert response.json() == {"data": {"team": expected}}


def test_get_team_missing(api_client):
    """
    Attempting to fetch a team that is missing should return an error
    message.
    """
    response = api_client.query(TEAM_QUERY, variables={"year": 2018})

    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(), "Team matching query does not exist.", path=["team"]
    )
