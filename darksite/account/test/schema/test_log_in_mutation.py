from unittest import mock

import pytest

from account import schema


class DummyInfo:
    def __init__(self, context):
        self.context = context


def test_log_in_invalid_credentials(db):
    """
    If the provided credentials don't match a user, an exception should
    be raised.
    """
    mutation = schema.LogIn()

    with pytest.raises(Exception):
        mutation.mutate(None, email='fake@example.com', password='password')


@mock.patch(
    'account.schema.login',
    autospec=True,
)
def test_log_in_valid_credentials(mock_login, rf, user_factory):
    """
    If valid credentials are provided to the mutation, the user with
    those credentials should be logged in and returned.
    """
    mutation = schema.LogIn()
    password = 'password'
    user = user_factory(password=password)

    request = rf.post('/')
    result = mutation.mutate(
        DummyInfo(request),
        email=user.email,
        password=password,
    )

    assert mock_login.call_count == 1
    assert result.user == user
