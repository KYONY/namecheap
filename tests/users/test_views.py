# tests/users/test_views.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestUserViewSet:
    def test_list_users_as_admin(self, admin_user, user_factory):
        """Test admin can see all users"""
        user1 = user_factory(username="test_user1")
        user2 = user_factory(username="test_user2")

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_user["access_token"]}')

        # Make request
        url = reverse('user-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK, \
            f"Expected 200 OK, got {response.status_code}"

        assert len(response.data) >= 3, \
            f"Expected at least 3 users, got {len(response.data)}. Data: {response.data}"

        usernames = [user['username'] for user in response.data]
        assert "admin" in usernames, "Admin user not found in response"
        assert "test_user1" in usernames, "test_user1 not found in response"
        assert "test_user2" in usernames, "test_user2 not found in response"

    def test_list_users_as_regular_user(self, authenticated_user):
        """Test regular user can only see themselves"""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {authenticated_user["access_token"]}')

        url = reverse('user-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK, \
            f"Expected 200 OK, got {response.status_code}"

        assert len(response.data) == 1, \
            f"Expected exactly 1 user, got {len(response.data)}. Data: {response.data}"

        assert response.data[0]['username'] == authenticated_user['user'].username, \
            f"Expected user {authenticated_user['user'].username}, got {response.data[0]['username']}"