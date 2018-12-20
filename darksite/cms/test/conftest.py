import factory
import pytest


class InfoPanelFactory(factory.DjangoModelFactory):
    """
    Factory for generating ``InfoPanel`` instances for testing.
    """
    text = 'The quick brown fox jumped over the lazy dog.'
    title = factory.Sequence(lambda n: f'Info Panel {n}')

    class Meta:
        model = 'cms.InfoPanel'


class MediaResourceFactory(factory.DjangoModelFactory):
    """
    Factory for generating ``MediaResource`` instances for testing.
    """
    youtube_id = factory.Sequence(lambda n: str(n))

    class Meta:
        model = 'cms.MediaResource'


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
