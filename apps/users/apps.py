# apps/users/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """
    Configuration class for the users application
    """
    # Full Python path to the application
    name = 'apps.users'

    # Human-readable name for the application
    verbose_name = _('Users Management')

    # Set default auto field for models
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        """
        Perform initialization tasks when the app is ready
        """
        try:
            # Import signal handlers
            import apps.users.signals  # noqa

            # Register any app-specific checks
            from django.core.checks import register, Tags
            from apps.users.checks import check_user_model_settings
            register(Tags.models)(check_user_model_settings)

        except ImportError:
            pass
