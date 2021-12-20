from rest_framework import serializers
from user.models import(
    User,
    Account,
    Session,
    VerificationToken
)


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        read_only_fields = [
            'password',
            'email_verified'
        ]
        fields = '__all__'


class AccountSerializer(serializers.Serializer):
    class Meta:
        model = Account
        fields = '__all__'


class SessionSerializer(serializers.Serializer):
    class Meta:
        model = Session
        fields = '__all__'


class VerificationTokenSerializer(serializers.Serializer):
    class Meta:
        model = VerificationToken
        fields = '__all__'
