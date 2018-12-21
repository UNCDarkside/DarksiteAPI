import factory


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
    image = factory.django.ImageField()

    class Meta:
        model = 'cms.MediaResource'
