import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Command to create an admin user using credentials from the
    environment.
    """

    help = (
        "Create an admin user using credentials found in the 'ADMIN_EMAIL' "
        "and 'ADMIN_PASSWORD' environment variables."
    )

    def handle(self, *args, **kwargs):
        """
        Execute the command.
        """
        email = os.environ["ADMIN_EMAIL"]
        password = os.environ["ADMIN_PASSWORD"]

        qs = get_user_model().objects.filter(email=email)
        if qs.exists():
            user = qs.get()
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.name = "Admin"
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Updated account '{email}' to have admin privileges."
                )
            )
        else:
            get_user_model().objects.create_superuser(
                email=email, name="Admin", password=password
            )

            self.stdout.write(
                self.style.SUCCESS(f"Created admin account '{email}'.")
            )
