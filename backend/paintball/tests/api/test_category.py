from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from paintball.models import (
    Category,
    User
)


class TestCategoriesAPI(APITestCase):

    def create_user(self, is_admin=False):
        if is_admin:
            user = User.objects.create_superuser(
                'admin',
                'admin@kingpaintball.com',
                'password'
            )
        else:
            user = User.objects.create_user(
                'user',
                'user@kingpaintball.com',
                'password'
            )

        token = Token.objects.create(user=user)

        return token

    # POST Requests

    def test_admin_create_categories(self):
        """
        Ensure that admins can create categories.
        """
        token = self.create_user(is_admin=True)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post('/api/categories/', {'name': 'marker'})
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_creates_categories(self):
        """
        Ensure that users can't create categories.
        """
        token = self.create_user(is_admin=False)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post('/api/categories/', {'name': 'marker'})
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET Requests

    def test_get_categories(self):
        """
        Ensure anyone can get categories.
        """
        Category.objects.create(name="marker")
        url = '/api/categories/1/'
        response = self.client.get(url)
        self.assertDictContainsSubset(
            {'id': 1, 'name': 'marker'}, response.data)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # PATCH Requests

    def test_admin_update_categories(self):
        """
        Ensure admin can update categories.
        """
        Category.objects.create(name="marker")
        token = self.create_user(is_admin=True)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.patch('/api/categories/1/', {'name': 'eclipse'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(
            {'id': 1, 'name': 'eclipse'}, response.data)

    def test_user_cant_update_categories(self):
        """
        Ensure user can't update categories.
        """
        Category.objects.create(name="marker")
        token = self.create_user(is_admin=False)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.patch('/api/categories/1/', {'name': 'eclipse'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE Requests

    def test_admin_delete_categories(self):
        """
        Ensure admin can delete categories.
        """
        Category.objects.create(name="marker")
        self.assertEqual(Category.objects.count(), 1)

        token = self.create_user(is_admin=True)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = '/api/categories/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_categories(self):
        """
        Ensure user cant delete categories.
        """
        Category.objects.create(name="marker")
        self.assertEqual(Category.objects.count(), 1)

        token = self.create_user(is_admin=False)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = '/api/categories/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
