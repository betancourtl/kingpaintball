from rest_framework.test import APITestCase
from rest_framework import status
from user.models import (
    User,
    Account,
)


class TestAccountAPI(APITestCase):

    def create_account(self):
        user = User.objects.create_user(
            'user1@kingpaintball.com',
            'password',
            name='Luis Betancourt',
        )

        account = Account.objects.create(
            type="type",
            provider="facebook",
            providerAccountId="123",
            refresh_token="refresh_token 123",
            access_token="access_token 123",
            expires_at=123456,
            token_type="JWT",
            scope="username,email,photo",
            id_token="123456",
            oauth_token_secret="oauth_token_secret",
            oauth_token="oauth_token",
            session_state="active",
            userId=user,
        )
        return account

    # POST

    def test_create_account(self):
        """Create an account"""

    # GET
    def test_get_one_account(self):
        """Get user account"""
        self.create_account()

        res = self.client.get('/api/accounts/1/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['provider'], 'facebook')

    # PATH

    def test_patch_account(self):
        """Patch the user"""
        self.create_account()

        res = self.client.patch('/api/accounts/1/', {
            'provider': 'github'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['provider'], 'github')

    # DELETE
    def test_delete_account(self):
        """Delete user"""
        self.create_account()

        res = self.client.delete('/api/accounts/1/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)
