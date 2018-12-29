from functional_tests import graphql_utils

LOG_IN_MUTATION = """
mutation LogInMutation($email: String!, $password: String!) {
  logIn(email: $email, password: $password) {
    user {
      id
      name
    }
  }
}
"""


def test_log_in(api_client, user_factory):
    """
    Users should be able to log in by providing their credentials.
    """
    password = "password"
    user = user_factory(password=password)

    response = api_client.mutate(
        LOG_IN_MUTATION, variables={"email": user.email, "password": password}
    )
    response.raise_for_status()

    assert response.status_code == 200
    assert response.json() == {
        "data": {"logIn": {"user": {"id": str(user.id), "name": user.name}}}
    }

    # The response should have a session cookie set
    assert "sessionid" in response.cookies


def test_log_in_invalid_credentials(api_client, user_factory):
    """
    Trying to log in with invalid credentials should raise an error.
    """
    user = user_factory(password="correct-password")

    response = api_client.mutate(
        LOG_IN_MUTATION,
        variables={"email": user.email, "password": "wrong-password"},
    )
    response.raise_for_status()

    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(),
        "No user with the provided email/password was found.",
        path=["logIn"],
    )

    # No session cookie should have been set
    assert "sessionid" not in response.cookies
