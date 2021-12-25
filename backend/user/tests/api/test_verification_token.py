from rest_framework.test import APITestCase
from rest_framework import status
from user.models import (
    VerificationToken,
)


class TestVerificationTokenAPI(APITestCase):
    # POST
    def test_create_token_verification(self):
        """Create token verification"""
        res = self.client.post('/api/verification-tokens/', {
            'token': 'token',
            'identifier': 'identifier',
        })

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset({
            'id': 1,
            'token': 'token',
            'identifier': 'identifier'
        }, res.data)
        self.assertEqual('expires' in res.data, True)

    # GET

    def test_get_token_verification(self):
        """Get token verification"""
        VerificationToken.objects.create(
            token='token',
            identifier='identifier'
        )
        res = self.client.get('/api/verification-tokens/1/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({
            'id': 1,
            'token': 'token',
            'identifier': 'identifier'
        }, res.data)
        self.assertEqual('expires' in res.data, True)

    # PATCH

    def test_patch_token_verification(self):
        """PATCH token verification"""
        VerificationToken.objects.create(
            token='token',
            identifier='identifier'
        )
        res = self.client.patch('/api/verification-tokens/1/', {
            'token': 'changed-token'
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['token'], 'changed-token')

    # DELETE
    def test_delete_token_verification(self):
        """Delete token verification"""
        VerificationToken.objects.create(
            token='token',
            identifier='identifier'
        )
        res = self.client.delete('/api/verification-tokens/1/')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VerificationToken.objects.count(), 0)
