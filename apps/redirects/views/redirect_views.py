# apps/redirects/views/redirect_views.py
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponseNotFound, HttpResponseForbidden
from apps.redirects.services.redirect_service import RedirectService
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class BaseRedirectView(View):
    """
    Base view for handling redirect requests
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redirect_service = RedirectService()
        self.jwt_authentication = JWTAuthentication()

    def get(self, request, identifier):
        """
        Handle GET requests for redirects
        """
        redirect_url = self.redirect_service.get_redirect_url(
            identifier=identifier,
            request=request
        )

        if not redirect_url:
            return HttpResponseNotFound("Redirect not found")

        return redirect(redirect_url)


class PublicRedirectView(BaseRedirectView):
    """
    View for handling public redirect requests
    """
    pass


@method_decorator(csrf_exempt, name='dispatch')
class PrivateRedirectView(BaseRedirectView):
    """
    View for handling private redirect requests
    """
    def get(self, request, identifier):
        try:
            # Аутентифікація за допомогою JWT
            auth_result = self.jwt_authentication.authenticate(request)
            if auth_result is not None:
                user, token = auth_result
                request.user = user
            else:
                return HttpResponseForbidden("Authentication required for private redirects")

            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required for private redirects")

            return super().get(request, identifier)

        except Exception as e:
            return HttpResponseForbidden(f"Authentication failed: {str(e)}")