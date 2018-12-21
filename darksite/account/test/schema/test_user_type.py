import uuid

import pytest

from account import schema, models


def test_resolve_user(user_factory):
    """
    Resolving a user by ID should return the user with the provided ID.
    """
    user = user_factory()
    query = schema.Query()

    assert query.resolve_user(None, id=user.id) == user


def test_resolve_user_invalid_id(db):
    """
    If there is no user with the provided ID, an exception should be
    raised.
    """
    query = schema.Query()

    with pytest.raises(models.User.DoesNotExist):
        query.resolve_user(None, id=uuid.uuid4())
