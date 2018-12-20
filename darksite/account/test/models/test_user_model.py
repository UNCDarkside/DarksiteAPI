from account import models


def test_create_superuser(db):
    """
    Test using the manager to create a superuser.
    """
    email = 'admin@example.com'
    name = 'Admin'
    password = 'password'

    models.User.objects.create_superuser(
        email=email,
        name=name,
        password=password,
    )
    user = models.User.objects.get()

    assert user.email == email
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser
    assert user.name == name
    assert user.check_password(password)


def test_create_user(db):
    """
    Test using the manager to create a new user.
    """
    email = 'john@example.com'
    name = 'John Smith'
    password = 'password'

    models.User.objects.create_user(
        email=email,
        name=name,
        password=password,
    )
    user = models.User.objects.get()

    assert user.email == email
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert user.name == name
    assert user.check_password(password)


def test_repr(user_factory):
    """
    The representation of the instance should return enough information
    to reconstruct the instance.
    """
    user = user_factory()
    expected = (
        f"User(email={repr(user.email)}, id={repr(user.id)}, "
        f"is_active={user.is_active}, is_staff={user.is_staff}, "
        f"is_superuser={user.is_superuser}, name={repr(user.name)})"
    )

    assert repr(user) == expected


def test_str():
    """
    The string representation of a user should include their name and
    email address.
    """
    user = models.User(email='john@example.com', name='John Smith')

    assert str(user) == f'{user.name} ({user.email})'
