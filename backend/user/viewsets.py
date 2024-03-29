from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework import viewsets
from user.models import (
    User,
    Account,
    Session,
    VerificationToken,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from user.serializers import (
    UserSerializer,
    AccountSerializer,
    SessionSerializer,
    VerificationTokenSerializer,
)


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    filterset_fields = [
        'email',
    ]


class AccountViewset(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = []
    filterset_fields = [
        'provider',
        'providerAccountId',
    ]


class SessionViewset(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = []
    filterset_fields = [
        'session_token',
    ]


class VerificationTokenViewset(viewsets.ModelViewSet):
    queryset = VerificationToken.objects.all()
    serializer_class = VerificationTokenSerializer
    permission_classes = []
    filterset_fields = [
        'identifier',
        'token'
    ]
