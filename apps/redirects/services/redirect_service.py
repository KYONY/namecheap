# apps/redirects/services/redirect_service.py
from typing import Optional, Union
from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from apps.redirects.models.redirect_rule import RedirectRule
from .identifier_generator import IdentifierGenerator


class RedirectService:
    """
    Service layer for handling redirect operations
    """
    def __init__(self):
        self.identifier_generator = IdentifierGenerator()

    @transaction.atomic
    def create_redirect(self, url: str, is_private: bool, user) -> RedirectRule:
        """
        Create a new redirect rule
        """
        existing_identifiers = set(
            RedirectRule.objects.values_list('redirect_identifier', flat=True)
        )

        identifier = self.identifier_generator.generate(existing_identifiers)

        return RedirectRule.objects.create(
            redirect_url=url,
            redirect_identifier=identifier,
            is_private=is_private,
            created_by=user
        )

    def get_redirect_url(self, identifier: str, request: HttpRequest) -> Optional[str]:
        """
        Get the redirect URL for a given identifier
        """
        redirect_rule = get_object_or_404(
            RedirectRule.objects.select_for_update(),
            redirect_identifier=identifier,
            is_active=True
        )

        # Check if private redirect is accessible
        if redirect_rule.is_private and not request.user.is_authenticated:
            return None

        # Increment click count in a separate transaction
        transaction.on_commit(
            lambda: redirect_rule.increment_click_count()
        )

        return redirect_rule.redirect_url

    def update_redirect(self, redirect_id: Union[str, int], data: dict, user) -> Optional[RedirectRule]:
        """
        Update an existing redirect rule
        """
        redirect = get_object_or_404(RedirectRule, id=redirect_id)

        # Check if user has permission to update
        if redirect.created_by != user and not user.is_staff:
            return None

        for key, value in data.items():
            setattr(redirect, key, value)

        redirect.save()
        return redirect

    def delete_redirect(self, redirect_id: Union[str, int], user) -> bool:
        """
        Delete a redirect rule
        """
        redirect = get_object_or_404(RedirectRule, id=redirect_id)

        # Check if user has permission to delete
        if redirect.created_by != user and not user.is_staff:
            return False

        redirect.delete()
        return True

    def get_user_redirects(self, user):
        """
        Get all redirects for a user
        """
        return RedirectRule.objects.filter(created_by=user).order_by('-created')
