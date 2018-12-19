import string

import markdown
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    """
    A single cms.blog post.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text=_('The user who wrote the post.'),
        null=True,
        on_delete=models.SET_NULL,
        related_name='blog_posts',
        related_query_name='blog_post',
        verbose_name=_('author'),
    )
    content = models.TextField(
        blank=True,
        help_text=_('The Markdown content of the post.'),
        verbose_name=_('content'),
    )
    published = models.DateTimeField(
        default=timezone.now,
        help_text=_('The time that the post should be published.'),
        verbose_name=_('publish time'),
    )
    slug = models.SlugField(
        help_text=_('A unique slug identifying the post.'),
        unique=True,
        verbose_name=_('slug'),
    )
    title = models.CharField(
        help_text=_('The title of the post.'),
        max_length=100,
        verbose_name=_('title'),
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text=_('The last time the post was updated.'),
        verbose_name=_('update time'),
    )

    class Meta:
        ordering = ('-published',)
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __repr__(self):
        """
        Returns:
            A string representation of the instance.
        """
        return (
            f"Post(author_id={repr(self.author.id)}, slug={repr(self.slug)})"
        )

    def __str__(self):
        """
        Returns:
            A user readable string describing the post.
        """
        return self.title

    def clean(self):
        """
        Generate a slug if necessary.
        """
        if not self.slug:
            suffix = get_random_string(
                length=10,
                allowed_chars=string.ascii_lowercase + string.digits,
            )

            self.slug = f'{slugify(self.title)}-{suffix}'

    @property
    def rendered(self):
        """
        Returns:
            An HTML version of the post's markdown content.
        """
        return markdown.markdown(
            self.content,
            output_format='html5',
        )
