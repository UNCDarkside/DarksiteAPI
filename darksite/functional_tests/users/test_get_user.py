import uuid

import requests

from functional_tests import graphql_utils

USER_QUERY = '''
query {{
  user(id: "{id}") {{
    id
    name
  }}
}}
'''


def test_get_user(live_server, user_factory):
    """
    Users should be able to retrieve information about users by their
    ID.
    """
    user = user_factory()
    expected = {
        'id': str(user.id),
        'name': user.name,
    }

    response = requests.get(
        f'{live_server.url}/graphql/',
        json={'query': USER_QUERY.format(id=user.id)},
    )
    response.raise_for_status()

    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'user': expected,
        },
    }


def test_get_user_invalid_id(live_server):
    """
    If there is no user with the provided ID, an error message should be
    returned.
    """
    response = requests.get(
        f'{live_server.url}/graphql/',
        json={'query': USER_QUERY.format(id=uuid.uuid4())},
    )
    response.raise_for_status()

    assert response.status_code == 200
    graphql_utils.assert_has_error(
        response.json(),
        'User matching query does not exist.',
        path=['user'],
    )
