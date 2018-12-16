from rest_framework import serializers

from blog import models


class PostListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for listing posts.
    """
    author_name = serializers.CharField(read_only=True, source='author.name')
    url = serializers.HyperlinkedIdentityField(
        lookup_field='slug',
        lookup_url_kwarg='post_slug',
        view_name='blog:post-detail',
    )

    class Meta:
        fields = (
            'url',
            'author_name',
            'published',
            'title',
            'slug',
            'updated',
        )
        model = models.Post


class PostDetailSerializer(PostListSerializer):
    """
    Serializer for a single post.
    """

    class Meta:
        fields = (
            'url',
            'author_name',
            'content',
            'published',
            'title',
            'rendered',
            'slug',
            'updated',
        )
        model = models.Post
