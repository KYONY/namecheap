# apps/redirects/views/management_views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.redirects.models.redirect_rule import RedirectRule
from apps.redirects.serializers.redirect_rule import RedirectRuleSerializer
from apps.redirects.services.redirect_service import RedirectService


class RedirectRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing redirect rules
    """
    serializer_class = RedirectRuleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'redirect_identifier'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redirect_service = RedirectService()

    def get_queryset(self):
        """
        Filter queryset based on user permissions
        """
        user = self.request.user
        if user.is_staff:
            return RedirectRule.objects.all()
        return RedirectRule.objects.filter(created_by=user)

    def perform_create(self, serializer):
        """
        Create a new redirect rule via service
        """
        redirect_rule = self.redirect_service.create_redirect(
            url=serializer.validated_data['redirect_url'],
            is_private=serializer.validated_data.get('is_private', False),
            user=self.request.user
        )
        serializer.instance = redirect_rule

    def perform_update(self, serializer):
        """
        Update redirect rule via service
        """
        redirect = self.redirect_service.update_redirect(
            redirect_id=serializer.instance.id,
            data=serializer.validated_data,
            user=self.request.user
        )

        if not redirect:
            return Response(
                {"detail": "You don't have permission to update this redirect"},
                status=status.HTTP_403_FORBIDDEN
            )

    def perform_destroy(self, instance):
        """
        Delete redirect rule via service
        """
        success = self.redirect_service.delete_redirect(
            redirect_id=instance.id,
            user=self.request.user
        )

        if not success:
            return Response(
                {"detail": "You don't have permission to delete this redirect"},
                status=status.HTTP_403_FORBIDDEN
            )

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get statistics for user's redirects
        """
        user_redirects = self.get_queryset()

        stats = {
            'total_redirects': user_redirects.count(),
            'total_clicks': sum(r.click_count for r in user_redirects),
            'private_redirects': user_redirects.filter(is_private=True).count(),
            'public_redirects': user_redirects.filter(is_private=False).count(),
        }

        return Response(stats)

    @action(detail=True, methods=['post'])
    def toggle_privacy(self, instance):
        """
        Toggle privacy status of a redirect
        """
        instance = self.get_object()
        instance.is_private = not instance.is_private
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_active(self, instance):
        """
        Toggle active status of a redirect
        """
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
