from django.test import (
    TestCase,
    Client,
)
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestAdminSite(TestCase):
    def setUp(self):
        self.client = Client()
        # Create an admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@kingpaintball.com',
            password='password123',
        )

        # Log in the superuser
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='user@kingpaintball.com',
            password='password123',
            name='user1'
        )

    def test_user_listed(self):
        """Test that users are listed in users page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_change_user_page(self):
        "Test that the user edit page works"
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        "Test that the user edit page works"
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
