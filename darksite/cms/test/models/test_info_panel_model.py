from cms import models


def test_create_no_media(db):
    """
    Test creating an info panel.
    """
    models.InfoPanel.objects.create(
        text="The quick brown fox jumped over the lazy dog.", title="No Media"
    )


def test_ordering(info_panel_factory):
    """
    Panels should be ordered by their ``order`` attribute.
    """
    p1 = info_panel_factory(order=2)
    p2 = info_panel_factory(order=3)
    p3 = info_panel_factory(order=1)

    assert list(models.InfoPanel.objects.all()) == [p3, p1, p2]


def test_repr():
    """
    The representation of the panel should contain the information
    necessary to reconstruct it.
    """
    panel = models.InfoPanel(title="Test Panel")
    expected = f"InfoPanel(id={repr(panel.id)}, title={repr(panel.title)})"

    assert repr(panel) == expected


def test_str():
    """
    Converting an info panel to a string should return the panel's
    title.
    """
    panel = models.InfoPanel(title="Test Panel")

    assert str(panel) == panel.title
