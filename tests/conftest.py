# tests/conftest.py
import os
import django
import pytest
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redirect_service.settings.local')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.redirects.models.redirect_rule import RedirectRule

User = get_user_model()

@pytest.fixture
def user_factory(db):
    def create_user(username="testuser", password="testpass123", is_staff=False):
        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=is_staff
        )
        user.save()  # Явне збереження
        return user
    return create_user

@pytest.fixture
def authenticated_user(user_factory):
    """Creates an authenticated user with JWT token."""
    user = user_factory()
    refresh = RefreshToken.for_user(user)
    return {
        'user': user,
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    }

@pytest.fixture
def admin_user(user_factory):
    """Creates an admin user with JWT token."""
    admin = user_factory(username="admin", is_staff=True)
    refresh = RefreshToken.for_user(admin)
    return {
        'user': admin,
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    }


@pytest.fixture
def redirect_rule_factory(db, authenticated_user):
    """Creates redirect rule instances."""
    def create_redirect_rule(
            redirect_url="https://example.com",
            is_private=False,
            is_active=True,
            created_by=None
    ):
        if created_by is None:
            created_by = authenticated_user['user']

        return RedirectRule.objects.create(
            redirect_url=redirect_url,
            is_private=is_private,
            is_active=is_active,
            created_by=created_by
        )
    return create_redirect_rule


@pytest.fixture(scope='function')
def db_reset(db):
    """Resets the database after each test."""
    yield
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM auth_user")