"""
Test fixtures used by all applications.
"""
import os

import factory
import pytest
from django.conf import settings


class UserFactory(factory.DjangoModelFactory):
    """
    Factory used to generate ``User`` instances for testing.
    """
    email = factory.Sequence(lambda n: f'test{n}@example.com')
    name = 'John Smith'
    password = 'password'

    class Meta:
        model = settings.AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Use our custom ``create_user`` method to create a new user.

        Args:
            model_class:
                The model class to instantiate.
            *args:
                Positional arguments used to create the user.
            **kwargs:
                Keyword arguments used to create the user.

        Returns:
            The new user instance.
        """
        manager = cls._get_manager(model_class)

        return manager.create_user(*args, **kwargs)


@pytest.fixture
def env():
    """
    Fixture that allows for modification of environment variables.
    After the test, the environment is rolled back to its previous
    state.

    Yields:
        A copy of the environment the test process is running in.
    """
    original_env = os.environ.copy()

    yield os.environ

    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def user_factory(db):
    """
    Returns:
        The factory used to create users for testing.
    """
    return UserFactory
