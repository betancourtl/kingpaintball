from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields: dict):
        """Creates a user using the custom user model.

        Args:
            email (str): Email of the user.

        Keyword Args:
            name (str): The name of the user.
            email_verified (str): If the email is verified.
            password (str): Password of the user.
            image (str): The image from the JWT token.
            is_staff (bool): If user is staff
            is_superuser (bool): If user is superuser
            is_active (bool): If user is active

        Raises:
            ValueError: Error when email is not valid

        Returns:
            User: the user user model instance
        """
        if not email:
            raise ValueError(_('The email must be set.'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str, **extra_fields: dict):
        """Creates a superuser

        Args:
            email ([type]): [description]

        Raises:
            ValueError: [description]
            ValueError: [description]

        Returns:
            [type]: [description]
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
