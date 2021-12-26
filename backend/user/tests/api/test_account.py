from pprint import pprint
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

    def test_create_facebook_account(self):
        """Create an account"""
        user = User.objects.create_user(
            'user1@kingpaintball.com',
            'password',
            name='Luis Betancourt',
        )

        res = self.client.post('/api/accounts/', {
            "provider": "facebook",
            "type": "oauth",
            "providerAccountId": "1411221565942028",
            "access_token": "EAANsTZBago9YBAI2NGn8m8wiebQOakZCg1yBhS2AXXRJH90G4zxnOfWWewtBklgOaiHD65OsypRPeCiLZBzW55TJJEiMBHzVvKqBKjCxwEZAUag9fScyRFHwQZB7k1vlSRSdZC2lZCihyrnz8ulabQaiITgpAZCZB1WaIhGtnBHpdgqsXVXBfny7ss71s7sTKZBt4AjbpoMdY8onWMatb8L3Pk8DbyZCBkkQGba7egNaTgZCNAZDZD",
            "token_type": "bearer",
            "expires_at": 1645653718,
            "userId": user.id,
        })

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)

    def test_create_google_account(self):
        """Create an account"""
        user = User.objects.create_user(
            'user1@kingpaintball.com',
            'password',
            name='Luis Betancourt',
        )

        res = self.client.post('/api/accounts/', {
            "provider": "google",
            "type": "oauth",
            "providerAccountId": "102408833001546",
            "access_token": "ya29.a0ARrdaM_FeEsdfsdfbvR1TyicvCwFOoRakECkTVDq9OzxFwfHDO3NtBRZK_PxhpEmK7uzgJA8X994w5gc83o1CB44oW5msOcKp-r08BlzZkT9UEvz0tvHre6KMlCY3touVoM_UuNtSfv_pBFT6IsMA",
            "expires_at": 1640481120,
            "scope": "openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
            "token_type": "Bearer",
            "id_token": "eyJhbGciOiJSUzI1NiIs234234234jAzZTg0YWVkNGVmNDQzMTAxNGU4NjE3NTY3ODY0YzRlZmFhYWVkZTkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI1NDUxNjQ3NTg3NjgtNG83N3RsMDcxMHVvZDdhanFqbXNtMGN0MW12bm50cmEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI1NDUxNjQ3NTg3NjgtNG83N3RsMDcxMHVvZDdhanFqbXNtMGN0MW12bm50cmEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDI0MDgyNjk2MzU4MzMwMDE1NDYiLCJlbWFpbCI6IndlYmRldmVsb3BlcnByQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiWE1jbEJaaXR1VGZPODRCT3hCdHl2dyIsIm5hbWUiOiJMdWlzIEJldGFuY291cnQiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2hDRTgxWHB5YzJyMk4xVTlpWTlsOTZLc09kNXBKNGtQVF9aNF92a3c9czk2LWMiLCJnaXZlbl9uYW1lIjoiTHVpcyIsImZhbWlseV9uYW1lIjoiQmV0YW5jb3VydCIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNjQwNDc3NTIzLCJleHAiOjE2NDA0ODExMjN9.UD0uv612vIStbP5km8UiibRxHuGaD7N_BEj-9IqqjdPguHzhFFnnU7agRm6KAfPOcwll7oK6LOhdeYWmmcmIT53B8IAOfEckiykxgu46PDEywy33MKY4i0f544kVBez5PZb-EfkoZ9D57jBs_xDLmTtVR3wfQyHF5TtN8Idcp65vx8IPx5yvhBFAtjxrTacmkvteELxMNzCyxUv47Zl2cYQo9peHY01Yud7Af3ya-aHQBo4jTxW6saFbM3ikQYwGlCNZMidrrz6zdzN3LPLQ6GAU0--HbgGfsexBuYUUQ_HtmKF7W9RYG4KW986LYlwz1IOhCmBgeBhZkvRSjDbABw",
            "userId": user.id
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)

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
