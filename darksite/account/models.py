import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from account import managers


class User(PermissionsMixin, AbstractBaseUser):
    """
    An authenticated user on the site.
    """
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'

    created = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time when the user was created.'),
        verbose_name=_('creation time'),
    )
    email = models.EmailField(
        help_text=_("The user's email address."),
        unique=True,
        verbose_name=_('email address'),
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        help_text=_('A unique identifier for the user.'),
        primary_key=True,
        verbose_name=_('ID'),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_('Designates if the user is allowed to log in.'),
        verbose_name=_('active status'),
    )
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Designates if the user has access to the admin site.'),
        verbose_name=_('admin status'),
    )
    last_login = models.DateTimeField(
        blank=True,
        help_text=_("The time of the user's last login."),
        null=True,
        verbose_name=_('last login time'),
    )
    name = models.CharField(
        help_text=_('A publicly displayed name for the user.'),
        max_length=100,
        verbose_name=_('name'),
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text=_('The last time the user was updated.'),
        verbose_name=_('update time'),
    )

    # Custom manager
    objects = managers.UserManager()

    class Meta:
        ordering = ('created',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __repr__(self):
        """
        Returns:
            A string containing the information needed to reconstruct
            the user.
        """
        return (
            f"User(email={repr(self.email)}, id={repr(self.id)}, "
            f"is_active={self.is_active}, is_staff={self.is_staff}, "
            f"is_superuser={self.is_superuser}, name={repr(self.name)})"
        )

    def __str__(self):
        """
        Returns:
            A user readable string describing the instance.
        """
        return f'{self.name} ({self.email})'
