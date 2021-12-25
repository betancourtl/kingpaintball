from pprint import pprint
from rest_framework.test import APITestCase
from user.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status


class TestUserAPI(APITestCase):
    # POST

    def test_create_user(self):
        """Creates a user"""
        res = self.client.post('/api/users/', {
            'name': 'admin',
            'email': 'admin@kingpaintball.com',
            'email_verified': 'asdf',
            'image': 'http://placehold.it/75x75',
        })

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    # GET

    def test_get_all_users(self):
        """Get all users"""
        User.objects.create_user(
            'user1@kingpaintball.com',
            'password'
        )
        User.objects.create_user(
            'user2@kingpaintball.com',
            'password'
        )

        res = self.client.get('/api/users/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    def test_get_one_user(self):
        """Get one user"""
        User.objects.create_user(
            'user1@kingpaintball.com',
            'password'
        )
        User.objects.create_user(
            'user2@kingpaintball.com',
            'password'
        )

        res = self.client.get('/api/users/2/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data['email'],
            'user2@kingpaintball.com'
        )

    def test_get_user_by_email(self):
        """Get one user"""
        User.objects.create_user(
            'user1@kingpaintball.com',
            'password'
        )
        User.objects.create_user(
            'user2@kingpaintball.com',
            'password'
        )

        res = self.client.get('/api/users/?email=user2@kingpaintball.com')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data['results'][0]['email'], 'user2@kingpaintball.com')

    # PATCH

    def test_patch_user(self):
        """Patch a user"""
        user = User.objects.create_user(
            'user1@kingpaintball.com',
            'password'
        )

        self.assertEqual(user.name, '')

        res = self.client.patch(
            '/api/users/1/',
            {'name': 'Luis'},
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(res.data['name'], 'Luis')

    # DELETE

    def test_delete_user(self):
        """Delete user"""
        User.objects.create_user(
            'user1@kingpaintball.com',
            'password'
        )

        res = self.client.delete('/api/users/1/')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
