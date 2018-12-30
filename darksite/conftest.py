"""
Test fixtures used by all applications.
"""
import io
import os

import factory
import pytest
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile

from cms.blog.test.factories import PostFactory
from cms.test.factories import (
    AlbumFactory,
    InfoPanelFactory,
    MediaResourceFactory,
)
from functional_tests.api_client import APIClient
from teams.test.factories import PersonFactory, TeamFactory


class UserFactory(factory.DjangoModelFactory):
    """
    Factory used to generate ``User`` instances for testing.
    """

    email = factory.Sequence(lambda n: f"test{n}@example.com")
    name = "John Smith"
    password = "password"

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
def album_factory(db):
    """
    Returns:
        The factory class used to create albums for testing.
    """
    return AlbumFactory


@pytest.fixture
def api_client(live_server):
    """
    Returns:
        An instance of the client used to interact with the GraphQL API.
    """
    return APIClient(f"{live_server.url}/graphql/")


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
def image():
    """
    Fixture to get an image suitable for an ``ImageField``.
    Returns:
        A ``ContentFile`` containing a simple image.
    """
    image = Image.new("RGB", (200, 200), "red")

    out_stream = io.BytesIO()
    image.save(out_stream, format="png")

    return ContentFile(content=out_stream.getvalue(), name="foo.png")


@pytest.fixture
def info_panel_factory(db):
    """
    Returns:
        The factory class used to generate info panels for testing.
    """
    return InfoPanelFactory


@pytest.fixture
def media_resource_factory(db):
    """
    Returns:
        The factory class used to generate media resources for testing.
    """
    return MediaResourceFactory


@pytest.fixture
def person_factory(db):
    """
    Returns:
        The factory class used to generate people for testing.
    """
    return PersonFactory


@pytest.fixture
def post_factory(db):
    """
    Returns:
        The factory class used to create posts for testing.
    """
    return PostFactory


@pytest.fixture
def team_factory(db):
    """
    Returns:
        The factory class used to create teams for testing.
    """
    return TeamFactory


@pytest.fixture
def user_factory(db):
    """
    Returns:
        The factory used to create users for testing.
    """
    return UserFactory
