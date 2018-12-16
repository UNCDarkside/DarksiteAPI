from django.db.models import Manager


class UserManager(Manager):
    """
    Manager for the User model.
    """

    def create_superuser(self, email, name, password, **kwargs):
        user = self.model(email=email, name=name, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, name, password, **kwargs):
        user = self.model(email=email, name=name, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def get_by_natural_key(self, email):
        """
        Lookup a user by their email address.
        Args:
            email:
                The email address of the user to get.

        Returns:
            The user with the given email.
        """
        return self.get(email=email)
