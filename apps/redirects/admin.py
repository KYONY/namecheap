# apps/redirects/admin.py
from django.contrib import admin
from django.utils.html import format_html
from apps.redirects.models.redirect_rule import RedirectRule

@admin.register(RedirectRule)
class RedirectRuleAdmin(admin.ModelAdmin):
    """
    Admin interface for RedirectRule model
    """
    list_display = ('redirect_identifier', 'get_redirect_url', 'created_by',
                    'is_private', 'created', 'modified', 'is_active', 'click_count')
    list_filter = ('is_private', 'is_active', 'created')
    search_fields = ('redirect_identifier', 'redirect_url', 'created_by__username')
    readonly_fields = ('redirect_identifier', 'created', 'modified')
    ordering = ('-created',)

    actions = ['make_private', 'make_public', 'activate', 'deactivate']

    fieldsets = (
        (None, {
            'fields': ('redirect_url', 'redirect_identifier', 'is_private')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Audit', {
            'fields': ('created_by', 'created', 'modified'),
            'classes': ('collapse',)
        }),
    )

    def get_redirect_url(self, obj):
        """
        Returns a clickable URL in admin interface
        """
        return format_html('<a href="{}" target="_blank">{}</a>',
                           obj.redirect_url, obj.redirect_url)
    get_redirect_url.short_description = 'Redirect URL'

    def save_model(self, request, obj, form, change):
        """
        Auto-set created_by field on save if it's a new object
        """
        if not change:  # If this is a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description='Mark selected rules as private')
    def make_private(self, request, queryset):
        updated = queryset.update(is_private=True)
        self.message_user(request, f'{updated} rules were marked as private.')

    @admin.action(description='Mark selected rules as public')
    def make_public(self, request, queryset):
        updated = queryset.update(is_private=False)
        self.message_user(request, f'{updated} rules were marked as public.')

    @admin.action(description='Activate selected rules')
    def activate(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} rules were activated.')

    @admin.action(description='Deactivate selected rules')
    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} rules were deactivated.')

    def get_queryset(self, request):
        """
        Override queryset to show all redirects to superusers,
        but only own redirects to regular staff
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def has_change_permission(self, request, obj=None):
        """
        Allow editing only if superuser or if user created the rule
        """
        if not obj or request.user.is_superuser:
            return True
        return obj.created_by == request.user

    def has_delete_permission(self, request, obj=None):
        """
        Allow deletion only if superuser or if user created the rule
        """
        if not obj or request.user.is_superuser:
            return True
        return obj.created_by == request.user
