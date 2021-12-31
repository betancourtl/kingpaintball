from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from paintball.models import (
    Condition,
)
from django.contrib.auth import get_user_model
User = get_user_model()


class TestConditionsAPI(APITestCase):

    def create_user(self, is_admin=False):
        if is_admin:
            user = User.objects.create_superuser(
                'admin@kingpaintball.com',
                'password'
            )
        else:
            user = User.objects.create_user(
                'user@kingpaintball.com',
                'password'
            )

        token = Token.objects.create(user=user)

        return token

    # POST Requests

    def test_admin_create_conditions(self):
        """
        Ensure that admins can create conditions.
        """
        token = self.create_user(is_admin=True)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post('/api/conditions/', {'name': 'new'})
        self.assertEqual(Condition.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_creates_conditions(self):
        """
        Ensure that users can't create conditions.
        """
        token = self.create_user(is_admin=False)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post('/api/conditions/', {'name': 'new'})
        self.assertEqual(Condition.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET Requests

    def test_get_conditions(self):
        """
        Ensure anyone can get conditions.
        """
        Condition.objects.create(name="new")
        url = '/api/conditions/1/'
        response = self.client.get(url)
        self.assertDictContainsSubset(
            {'id': 1, 'name': 'new'}, response.data)
        self.assertEqual(Condition.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # PATCH Requests

    def test_admin_update_conditions(self):
        """
        Ensure admin can update conditions.
        """
        Condition.objects.create(name="new")
        token = self.create_user(is_admin=True)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.patch('/api/conditions/1/', {'name': 'eclipse'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(
            {'id': 1, 'name': 'eclipse'}, response.data)

    def test_user_cant_update_conditions(self):
        """
        Ensure user can't update conditions.
        """
        Condition.objects.create(name="new")
        token = self.create_user(is_admin=False)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.patch('/api/conditions/1/', {'name': 'eclipse'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE Requests

    def test_admin_delete_conditions(self):
        """
        Ensure admin can delete conditions.
        """
        Condition.objects.create(name="new")
        self.assertEqual(Condition.objects.count(), 1)

        token = self.create_user(is_admin=True)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = '/api/conditions/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Condition.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_conditions(self):
        """
        Ensure user cant delete conditions.
        """
        Condition.objects.create(name="new")
        self.assertEqual(Condition.objects.count(), 1)

        token = self.create_user(is_admin=False)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = '/api/conditions/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Condition.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
