import pytest
from graphql import GraphQLError

from teams import schema, models


class Info:
    def __init__(self, context):
        self.context = context


def test_mutate(rf, user_factory):
    """
    Staff users should be able to execute the mutation by providing a
    name.
    """
    mutation = schema.CreatePerson()
    user = user_factory(is_staff=True)
    request = rf.post("/")
    request.user = user

    name = "Jane Smith"
    result = mutation.mutate(Info(request), name=name)

    assert result.person.name == name
    assert result.person.slug
    assert models.Person.objects.count() == 1


def test_mutate_non_staff(rf, user_factory):
    """
    If a non-staff user attempts to add a new person, an error should be
    thrown.
    """
    mutation = schema.CreatePerson()
    user = user_factory()
    request = rf.post("/")
    request.user = user

    with pytest.raises(GraphQLError):
        mutation.mutate(Info(request), name="John Doe")

    assert not models.Person.objects.exists()
