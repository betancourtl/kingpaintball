from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from paintball.models import (
    Brand,
)
from django.contrib.auth import get_user_model
User = get_user_model()


class TestBrandsAPI(APITestCase):

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

    def test_admin_create_brands(self):
        """
        Ensure that admins can create brands.
        """
        token = self.create_user(is_admin=True)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post('/api/brands/', {'name': 'marker'})
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_creates_brands(self):
        """
        Ensure that users can't create brands.
        """
        token = self.create_user(is_admin=False)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post('/api/brands/', {'name': 'marker'})
        self.assertEqual(Brand.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET Requests

    def test_get_brands(self):
        """
        Ensure anyone can get brands.
        """
        Brand.objects.create(name="marker")
        url = '/api/brands/1/'
        response = self.client.get(url)
        self.assertDictContainsSubset(
            {'id': 1, 'name': 'marker'}, response.data)
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # PATCH Requests

    def test_admin_update_brands(self):
        """
        Ensure admin can update brands.
        """
        Brand.objects.create(name="marker")
        token = self.create_user(is_admin=True)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.patch('/api/brands/1/', {'name': 'eclipse'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(
            {'id': 1, 'name': 'eclipse'}, response.data)

    def test_user_cant_update_brands(self):
        """
        Ensure user can't update brands.
        """
        Brand.objects.create(name="marker")
        token = self.create_user(is_admin=False)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.patch('/api/brands/1/', {'name': 'eclipse'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE Requests

    def test_admin_delete_brands(self):
        """
        Ensure admin can delete brands.
        """
        Brand.objects.create(name="marker")
        self.assertEqual(Brand.objects.count(), 1)

        token = self.create_user(is_admin=True)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = '/api/brands/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Brand.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_brands(self):
        """
        Ensure user cant delete brands.
        """
        Brand.objects.create(name="marker")
        self.assertEqual(Brand.objects.count(), 1)

        token = self.create_user(is_admin=False)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = '/api/brands/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
