# apps/users/serializers.py
from rest_framework import serializers
from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'created_at', 'updated_at')
#         read_only_fields = ('id', 'created_at', 'updated_at')
#
# class UserCreateSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')
#
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def to_representation(self, instance):
        # Детальна діагностика
        print(f"Serializing instance: {instance}")
        print(f"Instance type: {type(instance)}")

        try:
            rep = super().to_representation(instance)
            print(f"Serialized representation: {rep}")
            return rep
        except Exception as e:
            print(f"Serialization error: {e}")
            raise