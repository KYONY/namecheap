# tests/redirects/test_services.py
import pytest
from apps.redirects.services.redirect_service import RedirectService
from apps.redirects.services.identifier_generator import IdentifierGenerator

@pytest.mark.django_db
class TestRedirectService:
    def test_create_redirect(self, authenticated_user):
        """Test creating redirect through service."""
        service = RedirectService()
        redirect = service.create_redirect(
            url="https://example.com",
            is_private=False,
            user=authenticated_user['user']
        )
        assert redirect.redirect_url == "https://example.com"
        assert not redirect.is_private
        assert redirect.created_by == authenticated_user['user']

    def test_get_redirect_url(self, redirect_rule_factory):
        """Test getting redirect URL through service."""
        rule = redirect_rule_factory()
        service = RedirectService()
        url = service.get_redirect_url(rule.redirect_identifier, None)
        assert url == rule.redirect_url

class TestIdentifierGenerator:
    def test_generate_unique_identifier(self):
        """Test generating unique identifier."""
        generator = IdentifierGenerator()
        identifier1 = generator.generate()
        identifier2 = generator.generate()
        assert identifier1 != identifier2
        assert len(identifier1) == 8
