# apps/users/services.py
import uuid
from typing import Optional
from django.contrib.auth import get_user_model
from .models import User

class UserService:
    """
    Service layer for user-related operations
    """
    @staticmethod
    def create_user(username: str, password: str, email: Optional[str] = None) -> User:
        """
        Creates a new user instance
        """
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return user

    @staticmethod
    def get_user_by_id(user_id: uuid.UUID) -> Optional[User]:
        """
        Retrieves user by ID
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None