from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.managers import UserManager
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    """The User model is for information such as the user's name and email
    address. If a user first signs in with OAuth then their email address is
    automatically populated using the one from their OAuth profile, if the OAuth
    provider returns one.

    Args:
        AbstractBaseUser (class): Basic User class.
        PermissionsMixin (class): Add the fields and methods necessary to support the Group and Permission models using the ModelBackend.
    """
    name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, unique=True, db_index=True)  # AK
    email_verified = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=255, blank=True)
    # django specific
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.email


class Account(models.Model):
    """
    The Account model is for information about OAuth accounts associated with a
    User.
    """
    type = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    providerAccountId = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True)
    # used by github
    refresh_token_expires_in = models.IntegerField(null=True)
    access_token = models.CharField(max_length=255, blank=True)
    expires_at = models.IntegerField(null=True)
    token_type = models.CharField(max_length=255, blank=True)
    scope = models.CharField(max_length=255, blank=True)
    # used by google
    id_token = models.CharField(max_length=2000, blank=True)
    oauth_token_secret = models.CharField(max_length=255, blank=True)
    oauth_token = models.CharField(max_length=255, blank=True)
    session_state = models.CharField(max_length=255, blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.provider


class Session(models.Model):
    """
    The Session model is used for database sessions. It is not used if
    JSON Web Tokens are enabled.
    """
    expires = models.DateTimeField()
    session_token = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.session_token


class VerificationToken(models.Model):
    """
    The Verification Token model is used to store tokens for passwordless sign in.
    A single User can have multiple open Verification Tokens (e.g. to sign in
    to different devices).
    """
    token = models.CharField(max_length=255, unique=True, db_index=True)
    expires = models.DateTimeField()
    identifier = models.CharField(max_length=255)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.token
