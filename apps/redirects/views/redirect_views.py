# apps/redirects/views/redirect_views.py
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponseNotFound, HttpResponseForbidden
from rest_framework.permissions import IsAuthenticated
from apps.redirects.services.redirect_service import RedirectService


class RedirectView(View):
    """
    View for handling redirect requests
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redirect_service = RedirectService()
        self.private = kwargs.get('private', False)

    def get(self, request, identifier):
        """
        Handle GET requests for redirects
        """
        # Check authentication for private redirects
        if self.private and not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required for private redirects")

        # Get redirect URL from service
        redirect_url = self.redirect_service.get_redirect_url(
            identifier=identifier,
            request=request
        )

        if not redirect_url:
            return HttpResponseNotFound("Redirect not found")

        return redirect(redirect_url)
