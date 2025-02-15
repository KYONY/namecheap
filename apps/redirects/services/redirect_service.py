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
        Create a new redirect rule with unique identifier

        Args:
            url: The destination URL
            is_private: Whether the redirect requires authentication
            user: The user creating the redirect

        Returns:
            RedirectRule: The created redirect rule
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

    @transaction.atomic
    def get_redirect_url(self, identifier: str, request: HttpRequest) -> Optional[str]:
        """
        Get the redirect URL for a given identifier and handle click counting

        Args:
            identifier: The unique identifier for the redirect
            request: The HTTP request object for checking authentication

        Returns:
            Optional[str]: The destination URL if accessible, None otherwise
        """
        redirect_rule = get_object_or_404(
            RedirectRule.objects.select_for_update(),
            redirect_identifier=identifier,
            is_active=True
        )

        # Check if private redirect is accessible
        if redirect_rule.is_private and not request.user.is_authenticated:
            return None

        # Increment click count within the transaction
        redirect_rule.increment_click_count()

        return redirect_rule.redirect_url

    @transaction.atomic
    def update_redirect(self, redirect_id: Union[str, int], data: dict, user) -> Optional[RedirectRule]:
        """
        Update an existing redirect rule

        Args:
            redirect_id: The ID of the redirect to update
            data: Dictionary of fields to update
            user: The user attempting the update

        Returns:
            Optional[RedirectRule]: Updated redirect rule or None if not permitted
        """
        redirect = get_object_or_404(
            RedirectRule.objects.select_for_update(),
            id=redirect_id
        )

        # Check if user has permission to update
        if redirect.created_by != user and not user.is_staff:
            return None

        for key, value in data.items():
            if hasattr(redirect, key):
                setattr(redirect, key, value)

        redirect.save()
        return redirect

    @transaction.atomic
    def delete_redirect(self, redirect_id: Union[str, int], user) -> bool:
        """
        Delete a redirect rule

        Args:
            redirect_id: The ID of the redirect to delete
            user: The user attempting the deletion

        Returns:
            bool: True if deleted successfully, False if not permitted
        """
        redirect = get_object_or_404(
            RedirectRule.objects.select_for_update(),
            id=redirect_id
        )

        # Check if user has permission to delete
        if redirect.created_by != user and not user.is_staff:
            return False

        redirect.delete()
        return True

    def get_user_redirects(self, user):
        """
        Get all redirects for a user ordered by creation date

        Args:
            user: The user whose redirects to retrieve

        Returns:
            QuerySet: A queryset of RedirectRule objects
        """
        return RedirectRule.objects.filter(created_by=user).order_by('-created')

    def get_redirect_by_id(self, redirect_id: Union[str, int], user) -> Optional[RedirectRule]:
        """
        Get a specific redirect by ID with permission check

        Args:
            redirect_id: The ID of the redirect to retrieve
            user: The user attempting to access the redirect

        Returns:
            Optional[RedirectRule]: The redirect rule if accessible, None otherwise
        """
        redirect = get_object_or_404(RedirectRule, id=redirect_id)

        # Return redirect if user has permission
        if redirect.created_by == user or not redirect.is_private or user.is_staff:
            return redirect

        return None