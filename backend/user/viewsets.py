from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from user.models import (
    User,
    Account,
    Session,
    VerificationToken,
)

from user.serializers import (
    UserSerializer,
    AccountSerializer,
    SessionSerializer,
    VerificationTokenSerializer,
)


class UserViewset(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class AccountViewset(viewsets.ViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = []


class SessionViewset(viewsets.ViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = []


class VerificationTokenViewset(viewsets.ViewSet):
    queryset = VerificationToken.objects.all()
    serializer_class = VerificationTokenSerializer
    permission_classes = []
