# apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with basic validation
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')

    def to_representation(self, instance):
        """
        Override to ensure proper data transformation and debugging
        """
        try:
            data = super().to_representation(instance)
            return data
        except Exception as e:
            print(f"Error serializing user {instance.username}: {str(e)}")
            raise