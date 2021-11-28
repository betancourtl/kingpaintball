from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for our User model"""

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password',
            'name'
        )
