from django.test import TestCase
from django.contrib.auth import get_user_model
from paintball.models import Brand


class TestUserModel(TestCase):
    def test_create_user_with_email(self):
        """Test Creating user with email is successful"""
        email = 'admin@kingpaintball.com'
        password = '123456'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        "Test the email for a new user is normalized"
        email = "test@GMAIL.com"
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_valid_email(self):
        "Test creating user with no email raises error"

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '1234')

    def test_create_superuser(self):
        "Test creating a new superuser"

        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
