from django.test import TestCase
from user.models import Account
from django.contrib.auth import get_user_model

User = get_user_model()


class TestAccountModel(TestCase):

    def test_create_account(self):
        user = User.objects.create_user(
            'admin@kingpaintball.com',
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

        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(account.type, 'type')
        self.assertEqual(account.provider, 'facebook')
        self.assertEqual(account.providerAccountId, '123')
        self.assertEqual(account.refresh_token, 'refresh_token 123')
        self.assertEqual(account.access_token, 'access_token 123')
        self.assertEqual(account.expires_at, 123456)
        self.assertEqual(account.token_type, 'JWT')
        self.assertEqual(account.scope, 'username,email,photo')
        self.assertEqual(account.id_token, '123456')
        self.assertEqual(account.oauth_token_secret, 'oauth_token_secret')
        self.assertEqual(account.oauth_token, 'oauth_token')
        self.assertEqual(account.session_state, 'active')
        self.assertEqual(account.userId, user)
