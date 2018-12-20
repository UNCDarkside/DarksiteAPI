import graphene
import graphene_django
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from cms.blog import models


class PostType(graphene_django.DjangoObjectType):
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
        slug=graphene.String(
            description=_("The unique slug identifying the post.")
        )
    )
    posts = graphene.List(PostType)

    def resolve_post(self, info, slug=None, **kwargs):
        return models.Post.objects.get(
            published__lte=timezone.now(),
            slug=slug,
        )

    def resolve_posts(self, info, **kwargs):
        return models.Post.objects.filter(published__lte=timezone.now())
