from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from paintball.models import ( 
  Brand,
  Category,
  Condition,
  Item,
  Image,
  Like,
)


class TestItemsAPI(APITestCase):

    def with_foreign_props(self, dict1):
        category = Category.objects.create(name="marker")
        brand = Brand.objects.create(name="planet eclipse")
        condition = Condition.objects.create(name="used")
        user = User.objects.create(
          username="chewy",
          first_name="Luis",
          last_name="Betancourt",
          email="webdeveloperpr@gmail.com",
          password="123456",
          is_active=True
        )

        dict2 = {
          'category': category.id,
          'brand': brand.id,
          'condition': condition.id,
          'user': user.id,
        }

        return { **dict1, **dict2 }
    
    def test_create_items(self):
        """
        Ensure we can create items.
        """
        url = '/api/items/'
        data = self.with_foreign_props({
          'title': 'test title',
          'sold': True,
          'description': 'test description',
          'year': 2010,
          'price': 1200.00,
        })

        response = self.client.post(url, data, format='json')
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_items(self):
        """
        Ensure we can get items.
        """
        data = self.with_foreign_props({
          'title': 'test title',
          'sold': True,
          'description': 'test description',
          'year': 2010,
          'price': '1200.00',
        })

        self.client.post('/api/items/', data, format='json')
        
        response = self.client.get('/api/items/1/', {}, format='json')
        
        self.assertDictContainsSubset({ 
          'id': 1, 
          'title': data['title'],
          'sold': data['sold'],
          'description': data['description'],
          'year': data['year'],
          'price': data['price'],
        }, response.data)        
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_items(self):
        """
        Ensure we can update items.
        """
        self.client.post(
          '/api/items/', 
          self.with_foreign_props({
          'title': 'test title',
          'sold': True,
          'description': 'test description',
          'year': 2010,
          'price': '1200.00',
        }), 
          format='json'
        )
        
        new_data = {
          'title': 'new title',
          'sold': False,
          'description': 'new test description',
          'year': 2020,
          'price': '1199.99',
        }
        # Update the items
        response = self.client.patch('/api/items/1/', new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({ 
          'id': 1, 
          'title': new_data['title'],
          'sold': new_data['sold'],
          'description': new_data['description'],
          'year': new_data['year'],
          'price': new_data['price'],
        }, response.data)

    def test_delete_items(self):
        """
        Ensure we can get items.
        """
        self.client.post(
          '/api/items/', 
          self.with_foreign_props({
          'title': 'test title',
          'sold': True,
          'description': 'test description',
          'year': 2010,
          'price': '1200.00',
        }), 
          format='json'
        )

        # make sure there is only 1 item.
        self.assertEqual(Item.objects.count(), 1)

        url = '/api/items/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
