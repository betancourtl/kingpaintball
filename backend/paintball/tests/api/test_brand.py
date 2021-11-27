from rest_framework import status
from rest_framework.test import APITestCase
from paintball.models import ( 
  Brand
)


class TestBrandsAPI(APITestCase):

    def create_brands(self, brands_name):
        url = '/api/brands/'
        data = {
            'name': brands_name
        }
        response = self.client.post(url, data)
        return response
    
    def test_create_brands(self):
        """
        Ensure we can create brands.
        """
        response = self.create_brands('marker')
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_brands(self):
        """
        Ensure we can get brands.
        """
        self.create_brands('eclipse')
        
        url = '/api/brands/1/'
        data = { 'name': 'eclipse' }
        response = self.client.get(url, data, format='json')
        self.assertDictContainsSubset({ 'id': 1, 'name': 'eclipse' },response.data)
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_brands(self):
        """
        Ensure we can update brands.
        """
        self.create_brands('eclipse')

        # Update the brands
        response = self.client.patch('/api/brands/1/', {'name': 'eclipse'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({ 'id': 1, 'name': 'eclipse' },response.data)

    def test_delete_brands(self):
        """
        Ensure we can get brands.
        """
        self.create_brands('eclipse')

        # make sure there is only 1 item.
        self.assertEqual(Brand.objects.count(), 1)

        url = '/api/brands/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Brand.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
