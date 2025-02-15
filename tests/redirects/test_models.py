# tests/redirects/test_models.py
import pytest
from apps.redirects.models.redirect_rule import RedirectRule

@pytest.mark.django_db
class TestRedirectRuleModel:
    def test_create_redirect_rule(self, redirect_rule_factory):
        """Test creating a redirect rule."""
        rule = redirect_rule_factory()
        assert isinstance(rule, RedirectRule)
        assert rule.redirect_url == "https://example.com"
        assert not rule.is_private
        assert rule.is_active
        assert rule.redirect_identifier

    def test_increment_click_count(self, redirect_rule_factory):
        """Test incrementing click count."""
        rule = redirect_rule_factory()
        initial_count = rule.click_count
        rule.increment_click_count()
        assert rule.click_count == initial_count + 1
