from rest_framework import status
from rest_framework.test import APITestCase
from paintball.models import Brand


class BrandTests(APITestCase):

    def test_create_brands(self):
        """
        Ensure we can create brands.
        """
        url = '/api/brands/'
        data = {
            'name': 'eclipse'
        }
        response = self.client.post(url, data)
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_brands(self):
        """
        Ensure we can get brands.
        """
        url = '/api/brands/'
        response = self.client.get(url)
        self.assertEqual(Brand.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_brands(self):
        """
        Ensure we can update brands.
        """
        # Create 1 brand
        brand = Brand(name="dye")
        brand.save()

        # Update the brand
        response = self.client.patch('/api/brands/1/', {'name': 'eclipse'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'eclipse')

    def test_delete_brands(self):
        """
        Ensure we can get brands.
        """
        # Create 1 brand
        brand = Brand(name="dye")
        brand.save()

        # make sure there is only 1 item.
        self.assertEqual(Brand.objects.count(), 1)

        url = '/api/brands/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Brand.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
