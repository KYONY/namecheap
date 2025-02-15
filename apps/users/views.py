# apps/users/views.py
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    ViewSet for viewing users.

    Provides:
    - list: Get list of users (admin sees all, regular user sees only themselves)
    - retrieve: Get specific user details
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(pk=self.request.user.pk)

    def list(self, request, *args, **kwargs):
        """
        Override list method to add custom logic and better error handling
        """
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data)

        except Exception as e:
            print(f"Error in list view: {str(e)}")
            return Response(
                {"error": "Failed to retrieve users"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )