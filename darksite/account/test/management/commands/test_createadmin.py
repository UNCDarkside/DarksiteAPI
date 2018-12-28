from django.contrib.auth import get_user_model

from account.management.commands.createadmin import Command


def test_handle_new_user(db, env):
    """
    If the appropriate environment variables are present and the
    corresponding user doesn't exist in the database yet, they should
    be created.
    """
    env["ADMIN_EMAIL"] = "admin@example.com"
    env["ADMIN_PASSWORD"] = "password"

    command = Command()
    command.handle()

    user = get_user_model().objects.get()

    assert user.email == env["ADMIN_EMAIL"]
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser
    assert user.name == "Admin"
    assert user.check_password(env["ADMIN_PASSWORD"])


def test_handle_update_user(env, user_factory):
    """
    If the credentials provided to the command match an existing user,
    that user should be updated to be the new admin account.
    """
    env["ADMIN_EMAIL"] = "admin@example.com"
    env["ADMIN_PASSWORD"] = "new-password"

    user = user_factory(
        email=env["ADMIN_EMAIL"],
        is_active=False,
        is_staff=False,
        is_superuser=False,
        name="Not Admin",
    )

    command = Command()
    command.handle()

    user.refresh_from_db()

    assert user.email == env["ADMIN_EMAIL"]
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser
    assert user.name == "Admin"
    assert user.check_password(env["ADMIN_PASSWORD"])
