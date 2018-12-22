import factory

from test_utils import CleanAndSaveFactoryMixin


class PostFactory(CleanAndSaveFactoryMixin, factory.DjangoModelFactory):
    """
    Factory for generating ``Post`` instances for testing.
    """
    author = factory.SubFactory('conftest.UserFactory')
    title = factory.Sequence(lambda n: f'Post {n}')

    class Meta:
        model = 'blog.Post'
