from functional_tests import graphql_utils

CREATE_TEAM_MUTATION = """
mutation CreateTeamMutation($year: Int!) {
  createTeam(year: $year) {
    team {
      year
    }
  }
}
"""


def test_create_team(api_client, user_factory):
    """
    Staff users should be able to create a new team.
    """
    # Jim is a staff user on the site
    password = "password"
    user = user_factory(is_staff=True, password=password)

    # He logs in
    api_client.log_in(user.email, password)

    # Now he creates a new team
    year = 2018
    response = api_client.mutate(
        CREATE_TEAM_MUTATION, variables={"year": year}
    )

    # He receives a response containing the details of the team he just
    # created.
    assert response.status_code == 200, response.json()
    assert response.json() == {
        "data": {"createTeam": {"team": {"year": year}}}
    }


def test_create_team_non_unique(api_client, team_factory, user_factory):
    """
    Attempting to create a team for the same year as an existing team
    should raise an error.
    """
    # Jenny is a staff user on the site
    password = "password"
    user = user_factory(is_staff=True, password=password)

    # She logs in
    api_client.log_in(user.email, password)

    # There is a team already on the site.
    year = 2018
    team_factory(year=year)

    # She tries to create a team for the same year
    response = api_client.mutate(
        CREATE_TEAM_MUTATION, variables={"year": year}
    )

    # She receives an error because the team year is not unique
    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(),
        f"There is already a team for the year {year}.",
        path=["createTeam"],
    )


def test_create_team_not_staff(api_client, user_factory):
    """
    Non-staff users should receive an error message if they try to
    create a team.
    """
    # Jane is a normal user on the site.
    password = "password"
    user = user_factory(password=password)

    # She logs in
    api_client.log_in(user.email, password)

    # Now she tries to create a team
    response = api_client.mutate(
        CREATE_TEAM_MUTATION, variables={"year": 2018}
    )

    # She receives an error because she is not allowed to perform that
    # mutation.
    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(),
        "You do not have permission to create a team.",
        path=["createTeam"],
    )
