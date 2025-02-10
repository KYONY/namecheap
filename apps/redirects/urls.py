# apps/redirects/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.redirect_views import RedirectView
from .views.management_views import RedirectRuleViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'url', RedirectRuleViewSet, basename='redirect-rule')

urlpatterns = [
    # API endpoints for redirect management
    path('', include(router.urls)),

    # Redirect handling endpoints
    path('redirect/public/<str:identifier>/',
         RedirectView.as_view(private=False),
         name='public-redirect'),

    path('redirect/private/<str:identifier>/',
         RedirectView.as_view(private=True),
         name='private-redirect'),
]
