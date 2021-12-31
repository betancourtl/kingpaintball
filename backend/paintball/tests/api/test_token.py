from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestTokenClass(APITestCase):

    def test_post_token_with_valid_credentials(self):
        """Test that user can get their token"""

        User.objects.create_user(
            'user@kingpaintball.com',
            'password',
        )

        response = self.client.post('/token/', {
            'username': 'user@kingpaintball.com',
            'password': 'password'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_post_token_with_invalid_credentials(self):
        """Test that user can get their token"""

        User.objects.create_user(
            'user@kingpaintball.com',
            'password'
        )

        response = self.client.post('/token/', {
            'username': 'test@kingpaintball.com',
            'password': 'password'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
