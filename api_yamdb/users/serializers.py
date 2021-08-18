from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio',
        )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()


class UserCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=100)
