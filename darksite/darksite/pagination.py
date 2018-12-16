from rest_framework.pagination import CursorPagination


class PublishCursorPagination(CursorPagination):
    """
    Cursor pagination based on publish time.
    """
    ordering = ('-published',)
