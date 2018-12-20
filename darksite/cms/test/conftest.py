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


@pytest.fixture
def info_panel_factory(db):
    """
    Returns:
        The factory class used to generate info panels for testing.
    """
    return InfoPanelFactory
