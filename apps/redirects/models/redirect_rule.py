# apps/redirects/models/redirect_rule.py
import uuid
from django.db import models
from django.conf import settings
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _


class RedirectRule(models.Model):
    """
    Model for storing URL redirect rules
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    redirect_url = models.URLField(
        _('redirect URL'),
        max_length=2048,
        validators=[URLValidator()],
        help_text=_('The destination URL for the redirect')
    )

    redirect_identifier = models.CharField(
        _('redirect identifier'),
        max_length=50,
        unique=True,
        editable=False,
        help_text=_('Unique identifier for the redirect rule')
    )

    is_private = models.BooleanField(
        _('private status'),
        default=False,
        help_text=_('Whether this redirect requires authentication')
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_('Whether this redirect is active')
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='redirect_rules',
        verbose_name=_('created by')
    )

    created = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )

    modified = models.DateTimeField(
        _('modified at'),
        auto_now=True
    )

    click_count = models.PositiveIntegerField(
        _('click count'),
        default=0,
        help_text=_('Number of times this redirect has been used')
    )

    class Meta:
        verbose_name = _('redirect rule')
        verbose_name_plural = _('redirect rules')
        ordering = ['-created']
        indexes = [
            models.Index(fields=['redirect_identifier']),
            models.Index(fields=['created_by', 'is_active']),
        ]

    def __str__(self):
        return f"{self.redirect_identifier} -> {self.redirect_url}"

    def increment_click_count(self):
        """
        Increment the click count for this redirect
        """
        self.click_count += 1
        self.save(update_fields=['click_count'])