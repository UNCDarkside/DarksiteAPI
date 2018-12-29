import requests


LOG_IN_MUTATION = """
mutation LogIn($email: String!, $password: String!) {
  logIn(email: $email, password: $password) {
    user {
      id
    }
  }
}
"""


class APIClient(requests.Session):
    """
    A client used to interact with a GraphQL API.

    This is a thin wrapper around the :class:`requests.Session` class to
    add shortcut functions for running queries and mutations.
    """

    def __init__(self, url):
        """
        Create a new API client instance.

        Args:
            url:
                The URL of the GraphQL endpoint the client can interact
                with.
        """
        super().__init__()

        self.url = url

    def log_in(self, email, password):
        """
        Log in the client as a certain user.

        Args:
            email:
                The email of the user to log in as.
            password:
                The password of the user to log in as.
        """
        response = self.mutate(
            LOG_IN_MUTATION, variables={"email": email, "password": password}
        )
        response.raise_for_status()

        assert "errors" not in response.json()

    def mutate(self, mutation, **kwargs):
        """
        Run a mutation.

        Args:
            mutation:
                The mutation query to execute.
            **kwargs:
                Any additional information to pass to the GraphQL
                endpoint as data. The primary use of this is to pass
                variables in with a query.

        Returns:
            The :class:`requests.Response` instance containing the
            response from the API.
        """
        return self.post(self.url, json={"query": mutation, **kwargs})

    def query(self, query, **kwargs):
        """
        Execute a query.

        Args:
            query:
                The query to execute.
            **kwargs:
                Any additional information to pass to the GraphQL
                endpoint as data. The primary use of this is to pass
                variables in with a query.

        Returns:
            The :class:`requests.Response` instance containing the
            response from the API.
        """
        return self.get(self.url, json={"query": query, **kwargs})
