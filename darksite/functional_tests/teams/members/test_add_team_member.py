from functional_tests import graphql_utils

ADD_TEAM_MEMBER_MUTATION = """
mutation AddTeamMember(
  $number: Int,
  $personSlug: String!,
  $role: String!,
  $teamYear: Int!
) {
  addTeamMember(
    number: $number,
    personSlug: $personSlug,
    role: $role,
    teamYear: $teamYear
  ) {
    teamMember {
      number
      person {
        name
        slug
      }
      role
      team {
        year
      }
    }
  }
}
"""


def test_add_team_member_coach(
    api_client, person_factory, team_factory, user_factory
):
    """
    Staff users should be able to add an existing person to an existing
    team as a coach.
    """
    # Given an existing person and team...
    person = person_factory()
    team = team_factory()

    # Ginny, an existing staff user...
    password = "password"
    user = user_factory(is_staff=True, name="Ginny", password=password)

    # ...logs in and associates the existing person with a team as a
    # coach.
    api_client.log_in(user.email, password)
    response = api_client.mutate(
        ADD_TEAM_MEMBER_MUTATION,
        variables={
            "personSlug": person.slug,
            "role": "C",
            "teamYear": team.year,
        },
    )
    response.raise_for_status()

    # She receives a response with the information of the created team
    # member.
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "addTeamMember": {
                "teamMember": {
                    "number": None,
                    "person": {"name": person.name, "slug": person.slug},
                    "role": "C",
                    "team": {"year": team.year},
                }
            }
        }
    }


def test_add_team_member_invalid_person_slug(
    api_client, team_factory, user_factory
):
    """
    If there is no person with the provided person slug, an error should
    be returned.
    """
    # Given an existing team...
    team = team_factory()

    # Bill, an existing staff user...
    password = "password"
    user = user_factory(is_staff=True, name="Bill", password=password)

    # ...logs in and attempts to add a team member using a slug that
    # does not correspond to any person.
    api_client.log_in(user.email, password)
    slug = "non-existent"
    response = api_client.mutate(
        ADD_TEAM_MEMBER_MUTATION,
        variables={"personSlug": slug, "role": "C", "teamYear": team.year},
    )

    # He receives an error message stating the person doesn't exist.
    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(),
        f'The person with the slug "{slug}" does not exist.',
        path=["addTeamMember"],
    )


def test_add_team_member_invalid_team_year(
    api_client, person_factory, user_factory
):
    """
    Attempting to use an invalid role should return an error message.
    """
    # Given an existing person...
    person = person_factory()

    # Jennifer, an existing staff user...
    password = "password"
    user = user_factory(is_staff=True, name="Jennifer", password=password)

    # ...logs in and attempts to create a team member, but she
    # accidentally specifies a team year that doesn't exist yet.
    api_client.log_in(user.email, password)
    year = 2018
    response = api_client.mutate(
        ADD_TEAM_MEMBER_MUTATION,
        variables={"personSlug": person.slug, "role": "C", "teamYear": year},
    )

    # Since the year is invalid, she receives an error response.
    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(),
        f"The team for the year {year} does not exist.",
        path=["addTeamMember"],
    )


def test_add_team_member_non_staff(
    api_client, person_factory, team_factory, user_factory
):
    """
    Non staff users should receive a permissions error if they attempt
    to create a new team member.
    """
    # Given an existing team and person...
    person = person_factory()
    team = team_factory()

    # Sally, an existing non-staff user...
    password = "password"
    user = user_factory(name="Sally", password=password)

    # ...logs in and attempts to create a new team member.
    api_client.log_in(user.email, password)
    response = api_client.mutate(
        ADD_TEAM_MEMBER_MUTATION,
        variables={
            "personSlug": person.slug,
            "role": "C",
            "teamYear": team.year,
        },
    )

    # She receives an error message because she is not a staff user.
    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(),
        "You do not have permission to add a team member.",
        path=["addTeamMember"],
    )


def test_add_team_member_non_unique(
    api_client, team_member_factory, user_factory
):
    """
    If a team member already exists, attempting to add them again should
    return an error message.
    """
    # Given an existing team member...
    member = team_member_factory()

    # Charlie, an existing staff user...
    password = "password"
    user = user_factory(is_staff=True, name="Charlie", password=password)

    # ...logs in and attempts to recreate a team member that already
    # exists.
    api_client.log_in(user.email, password)
    response = api_client.mutate(
        ADD_TEAM_MEMBER_MUTATION,
        variables={
            "personSlug": member.person.slug,
            "role": "C",
            "teamYear": member.team.year,
        },
    )

    # He receives an error message stating that the team member already
    # exists.
    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(),
        (
            f"{member.person.name} is already a member of the "
            f"{member.team.year} team."
        ),
        path=["addTeamMember"],
    )


def test_add_team_member_player(
    api_client, person_factory, team_factory, user_factory
):
    """
    Staff users should be able to add an existing person to an existing
    team as a player.
    """
    # Given an existing person and team...
    person = person_factory()
    team = team_factory()

    # George, an existing staff user...
    password = "password"
    user = user_factory(is_staff=True, name="George", password=password)

    # ...logs in and associates the existing person with a team as a
    # player.
    api_client.log_in(user.email, password)
    response = api_client.mutate(
        ADD_TEAM_MEMBER_MUTATION,
        variables={
            "number": 42,
            "personSlug": person.slug,
            "role": "P",
            "teamYear": team.year,
        },
    )
    response.raise_for_status()

    # He receives a response with the information of the created team
    # member.
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "addTeamMember": {
                "teamMember": {
                    "number": 42,
                    "person": {"name": person.name, "slug": person.slug},
                    "role": "P",
                    "team": {"year": team.year},
                }
            }
        }
    }
