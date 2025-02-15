# apps/redirects/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.redirects.views.management_views import RedirectRuleViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'url', RedirectRuleViewSet, basename='redirect-rule')

urlpatterns = [
    path('', include(router.urls)),
]