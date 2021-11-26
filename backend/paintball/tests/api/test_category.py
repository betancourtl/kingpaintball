from rest_framework import status
from rest_framework.test import APITestCase
from paintball.models import ( 
  Category
)


class TestCategoryAPI(APITestCase):

    def create_category(self, category_name):
        url = '/api/categories/'
        data = {
            'name': category_name
        }
        response = self.client.post(url, data)
        return response
    
    def test_create_category(self):
        """
        Ensure we can create category.
        """
        response = self.create_category('marker')
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_category(self):
        """
        Ensure we can get category.
        """
        self.create_category('marker')
        
        url = '/api/categories/1/'
        data = { 'name': 'marker' }
        response = self.client.get(url, data, format='json')
        self.assertDictContainsSubset({ 'id': 1, 'name': 'marker' },response.data)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        """
        Ensure we can update category.
        """
        self.create_category('marker')

        # Update the category
        response = self.client.patch('/api/categories/1/', {'name': 'tank'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({ 'id': 1, 'name': 'tank' },response.data)

    def test_delete_category(self):
        """
        Ensure we can get category.
        """
        self.create_category('marker')

        # make sure there is only 1 item.
        self.assertEqual(Category.objects.count(), 1)

        url = '/api/categories/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
