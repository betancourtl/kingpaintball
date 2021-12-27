from rest_framework import serializers
from user.models import(
    User,
    Account,
    Session,
    VerificationToken
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = [
            'password',
            # 'email_verified'
        ]
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class VerificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationToken
        fields = '__all__'
