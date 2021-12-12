from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from paintball.models import (
    Brand,
    Category,
    Condition,
    Like,
    User,
    Item,
)


class TestTokenClass(APITestCase):

    def test_post_token_with_valid_credentials(self):
        """Test that user can get their token"""

        user = User.objects.create_user(
            'user',
            'user@kingpaintball.com',
            'password'
        )

        response = self.client.post('/token/', {
            'username': 'user',
            'password': 'password'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_post_token_with_invalid_credentials(self):
        """Test that user can get their token"""

        user = User.objects.create_user(
            'user',
            'user@kingpaintball.com',
            'password'
        )

        response = self.client.post('/token/', {
            'username': 'none',
            'password': 'password'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
