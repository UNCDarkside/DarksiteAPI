from cms import models
from functional_tests import serializer_utils

INFO_PANEL_LIST_QUERY = """
query {
  infoPanels {
    id
    media {
      caption
      created
      id
      image
      title
      type
      youtubeId
    }
    text
    title
  }
}
"""


def test_list_info_panels(
    api_client, image, info_panel_factory, live_server, media_resource_factory
):
    """
    Users should be able to list the info panels that exist through the
    API.
    """
    image_resource = media_resource_factory(image=image)
    video_resource = media_resource_factory(youtube_id="dQw4w9WgXcQ")

    info_panel_factory(
        media=image_resource, text="A panel with an image.", title="Panel 1"
    )
    info_panel_factory(
        media=video_resource, text="A panel with a video.", title="Panel 2"
    )
    info_panel_factory(text="A panel with no media.", title="Panel 3")

    expected = []
    for panel in models.InfoPanel.objects.all():
        expected.append(
            {
                "id": str(panel.id),
                "media": serializer_utils.serialize_media_resource(
                    panel.media, live_server.url
                ),
                "text": panel.text,
                "title": panel.title,
            }
        )

    response = api_client.query(INFO_PANEL_LIST_QUERY)
    response.raise_for_status()

    assert response.status_code == 200
    assert response.json() == {"data": {"infoPanels": expected}}
