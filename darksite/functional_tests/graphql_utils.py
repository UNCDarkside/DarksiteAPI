def assert_has_error(response, message, path=None):
    """
    Assert that a GraphQL response has a certain error.

    Args:
        response:
            The response to check for the error in.
        message:
            The error message that should be contained.
        path:
            An optional path that the error should have occurred at. If
            not specified, this is not checked.
    """
    criteria = [('message', message)]
    if path is not None:
        criteria.append(('path', path))

    assert len(response.get('errors', [])) > 0, (
        'The response has no errors.'
    )

    for error in response['errors']:
        if _error_matches_criteria(error, criteria):
            return

    assert False, (
        'No message found with the criteria: {}'
    ).format(criteria)


def _error_matches_criteria(error, criteria):
    """
    Check if an error matches a set of criteria.

    Args:
        error:
            The error to check.
        criteria:
            A list of key value pairs to check for in the error.

    Returns:
        A boolean indicating if the provided error matches the given
        criteria.
    """
    for key, value in criteria:
        if error.get(key) != value:
            return False

    return True
