import uuid

from functional_tests import graphql_utils

USER_QUERY = """
query GetUserByID($id: UUID!) {
  user(id: $id) {
    id
    name
  }
}
"""


def test_get_user(api_client, user_factory):
    """
    Users should be able to retrieve information about users by their
    ID.
    """
    user = user_factory()
    expected = {"id": str(user.id), "name": user.name}

    response = api_client.query(USER_QUERY, variables={"id": str(user.id)})
    response.raise_for_status()

    assert response.status_code == 200
    assert response.json() == {"data": {"user": expected}}


def test_get_user_invalid_id(api_client):
    """
    If there is no user with the provided ID, an error message should be
    returned.
    """
    response = api_client.query(
        USER_QUERY, variables={"id": str(uuid.uuid4())}
    )
    response.raise_for_status()

    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(), "User matching query does not exist.", path=["user"]
    )
