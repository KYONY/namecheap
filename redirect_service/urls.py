"""
URL configuration for redirect_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from apps.redirects.views.redirect_views import PublicRedirectView, PrivateRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Redirect endpoints according to specification
    path('redirect/public/<str:identifier>', PublicRedirectView.as_view(), name='public-redirect'),
    path('redirect/private/<str:identifier>', PrivateRedirectView.as_view(), name='private-redirect'),

    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/redirects/', include('apps.redirects.urls')),
]
