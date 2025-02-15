# tests/users/test_models.py
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self, user_factory):
        user = user_factory()
        assert user.username == "testuser"
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username="admin",
            password="admin123"
        )
        assert admin.is_superuser
        assert admin.is_staff
