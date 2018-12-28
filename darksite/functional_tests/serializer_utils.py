def serialize_media_resource(media, base_url):
    """
    Serialize a media resource.

    Args:
        media:
            The media resource to serialize.
        base_url:
            The base URL of the server that the request was made to.

    Returns:
        A serialized version of the media resource. If the media
        resource is not truthy, ``None`` is returned instead.
    """
    if not media:
        return None

    return {
        "caption": media.caption,
        "created": media.created.isoformat(),
        "id": str(media.id),
        "image": _file_url(media.image, base_url),
        "title": media.title,
        "type": media.type,
        "youtubeId": media.youtube_id or None,
    }


def _file_url(file, base_url):
    """
    Get the full URL of a file.

    Args:
        file:
            The file to get the URL of.
        base_url:
            The base URL to append the file's absolute URL to.

    Returns:
        The full URL of the given file if it exists or ``None`` if it
        doesn't.
    """
    if not file:
        return None

    return f"{base_url}{file.url}"
