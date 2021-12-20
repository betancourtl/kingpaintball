from django.test import TestCase
from django.db.utils import IntegrityError
from user.models import User


class TestUserModel(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            'admin@kingpaintball.com',
            'password',
            name='Luis Betancourt',
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.name, 'Luis Betancourt')
        self.assertEqual(user.email, 'admin@kingpaintball.com')

    def test_create_super_user(self):
        user = User.objects.create_superuser(
            'admin@kingpaintball.com',
            'password',
            name='Luis Betancourt',
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.name, 'Luis Betancourt')
        self.assertEqual(user.email, 'admin@kingpaintball.com')
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)
