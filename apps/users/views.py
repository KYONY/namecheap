# apps/users/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from .services import UserService


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         user = self.request.user
#         # todo dell
#         print(f"Current user: {self.request.user}")
#         print(f"Is authenticated: {self.request.user.is_authenticated}")
#         print(f"Is staff: {self.request.user.is_staff}")
#
#         if not self.request.user.is_authenticated:
#             return User.objects.none()
#
#         if user.is_staff:
#             queryset = User.objects.all()
#             # todo dell
#             print(f"All users count: {queryset.count()}")  # Друк кількості користувачів
#
#             return queryset
#
#         return User.objects.filter(id=user.id)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f"Request user: {self.request.user}")
        print(f"Is authenticated: {self.request.user.is_authenticated}")
        print(f"Is staff: {self.request.user.is_staff}")

        # Детальна діагностика користувачів
        all_users = User.objects.all()
        print("All users in DB:", list(all_users.values_list('username', flat=True)))

        if self.request.user.is_staff:
            return all_users
        return User.objects.filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        try:
            # Примусове отримання QuerySet
            queryset = self.get_queryset()

            # Додаткова діагностика
            print("Queryset in list method:", list(queryset))

            # Серіалізація з явним контекстом
            serializer = self.get_serializer(
                queryset,
                many=True,
                context={'request': request}
            )

            print("Serialized data:", serializer.data)
            return Response(serializer.data)

        except Exception as e:
            print(f"Error in list method: {e}")
            return Response([])