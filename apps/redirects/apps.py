# apps/redirects/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RedirectsConfig(AppConfig):
    """
    Configuration class for the redirects application
    """
    name = 'apps.redirects'
    verbose_name = _('URL Redirects')
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        """
        Perform initialization tasks when the app is ready
        """
        try:
            # Import signal handlers
            import apps.redirects.signals  # noqa

            # Register any app-specific checks
            from django.core.checks import register, Tags
            from apps.redirects.checks import check_redirect_settings
            register(Tags.models)(check_redirect_settings)

        except ImportError:
            pass
