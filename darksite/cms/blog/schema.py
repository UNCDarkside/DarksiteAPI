import graphene
import graphene_django
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from cms.blog import models


class PostType(graphene_django.DjangoObjectType):
    """
    A blog post.
    """
    rendered = graphene.String(
        description=_("The rendered HTML of the post's Markdown content."),
    )

    class Meta:
        only_fields = (
            'author',
            'content',
            'published',
            'slug',
            'title',
            'updated',
        )
        model = models.Post


class Query(graphene.ObjectType):
    post = graphene.Field(
        PostType,
        description=_('Query for a specific post.'),
        slug=graphene.String(
            description=_("The unique slug identifying the post.")
        )
    )
    posts = graphene.List(
        PostType,
        description=_('Query for a list of posts.'),
    )

    @staticmethod
    def resolve_post(*args, slug=None, **kwargs):
        """
        Resolve a single blog post.

        Args:
            slug:
                The slug of the post to retrieve.

        Returns:
            The post with the given slug if it has been published.
        """
        return models.Post.objects.get(
            published__lte=timezone.now(),
            slug=slug,
        )

    @staticmethod
    def resolve_posts(*args, **kwargs):
        """
        Resolve the list of published blog posts.

        Returns:
            A queryset of the blog posts that have been published.
        """
        return models.Post.objects.filter(published__lte=timezone.now())
