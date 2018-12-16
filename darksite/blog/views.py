from django.utils import timezone
from rest_framework import generics

from blog import models, serializers
from darksite import pagination


class PostDetailView(generics.RetrieveAPIView):
    """
    get:
    Retrieve a single blog post.
    """
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'
    serializer_class = serializers.PostDetailSerializer

    def get_queryset(self):
        """
        Limit the queryset to published posts.

        Returns:
            All the posts that have been published.
        """
        return models.Post.objects.filter(published__lte=timezone.now())


class PostListView(generics.ListAPIView):
    """
    get:
    List all published blog posts.
    """
    pagination_class = pagination.PublishCursorPagination
    serializer_class = serializers.PostListSerializer

    def get_queryset(self):
        return models.Post.objects.filter(published__lte=timezone.now())
