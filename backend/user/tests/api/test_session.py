from rest_framework.test import APITestCase
from rest_framework import status
from user.models import (
    User,
    Session,
)


class TestSessionAPI(APITestCase):
    def create_session(self):
        user = User.objects.create_user(
            'user1@kingpaintball.com',
            'password',
            name='Luis Betancourt',
        )
        session = Session.objects.create(
            session_token='session_token',
            userId=user
        )

        return session

        # POST

    def test_create_session(self):
        """Create session"""

    # GET

    def test_get_session(self):
        """Get user"""
        self.create_session()
        res = self.client.get('/api/sessions/1/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # PATCH

    def test_patch_session(self):
        "Patch session"
        self.create_session()
        res = self.client.patch('/api/sessions/1/', {
            'session_token': 'new_session_token'
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['session_token'], 'new_session_token')

    # DELETE

    def test_delete_session(self):
        self.create_session()
        res = self.client.delete('/api/sessions/1/')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Session.objects.count(), 0)
