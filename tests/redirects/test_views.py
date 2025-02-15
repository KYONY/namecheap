# tests/redirects/test_views.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

class TestRedirectViews:
    def test_create_redirect_rule(self, api_client, authenticated_user):
        """Test creating a new redirect rule."""
        url = reverse('redirect-rule-list')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {authenticated_user["access_token"]}')
        data = {
            'redirect_url': 'https://example.com',
            'is_private': False
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_public_redirect(self, api_client, redirect_rule_factory):
        """Test accessing public redirect."""
        rule = redirect_rule_factory(is_private=False)
        url = reverse('public-redirect', kwargs={'identifier': rule.redirect_identifier})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_302_FOUND

    def test_private_redirect_without_auth(self, api_client, redirect_rule_factory):
        """Test accessing private redirect without authentication."""
        rule = redirect_rule_factory(is_private=True)
        url = reverse('private-redirect', kwargs={'identifier': rule.redirect_identifier})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_private_redirect_with_auth(self, api_client, authenticated_user, redirect_rule_factory):
        """Test accessing private redirect with authentication."""
        rule = redirect_rule_factory(is_private=True)
        url = reverse('private-redirect', kwargs={'identifier': rule.redirect_identifier})
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {authenticated_user["access_token"]}')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
