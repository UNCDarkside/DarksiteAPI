from functional_tests import graphql_utils

CREATE_PERSON_MUTATION = """
mutation CreatePerson($name: String!) {
  createPerson(name: $name) {
    person {
      name
      slug
    }
  }
}
"""


def test_create_person(api_client, user_factory):
    """
    Staff users should be able to create people.
    """
    # Jimbo is a staff user.
    password = "password"
    user = user_factory(is_staff=True, name="Jimbo", password=password)

    # He logs in...
    api_client.log_in(user.email, password)

    # He creates a new person...
    name = "John Smith"
    slug = "john-smith"
    response = api_client.mutate(
        CREATE_PERSON_MUTATION, variables={"name": name}
    )
    response.raise_for_status()

    # Then he receives the details of the newly created person...
    assert response.status_code == 200
    assert response.json() == {
        "data": {"createPerson": {"person": {"name": name, "slug": slug}}}
    }


def test_create_person_non_staff(api_client, user_factory):
    """
    If a non-staff user attempts to add a new person they should receive
    a permissions error.
    """
    # Jane is a normal user.
    password = "password"
    user = user_factory(name="Jane", password=password)

    # She logs in...
    api_client.log_in(user.email, password)

    # She attempts to create a new person...
    response = api_client.mutate(
        CREATE_PERSON_MUTATION, variables={"name": "John Smith"}
    )
    response.raise_for_status()

    # She receives an error message.
    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(),
        "You do not have permission to create a new person.",
        path=["createPerson"],
    )
