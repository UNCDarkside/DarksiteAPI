import factory
import pytest


class PostFactory(factory.DjangoModelFactory):
    """
    Factory for generating ``Post`` instances for testing.
    """
    author = factory.SubFactory('conftest.UserFactory')
    title = factory.Sequence(lambda n: f'Post {n}')

    class Meta:
        model = 'blog.Post'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Create a model instance, clean it, and save it.

        Args:
            model_class:
                The model class to create an instance of.
            *args:
                The positional arguments to instantiate the model with.
            **kwargs:
                The keyword arguments to instantiate the model with.
        Returns:
            The created model instance.
        """
        instance = model_class(*args, **kwargs)
        instance.clean()
        instance.save()

        return instance


@pytest.fixture
def post_factory(db):
    """
    Returns:
        The factory class used to create posts for testing.
    """
    return PostFactory
