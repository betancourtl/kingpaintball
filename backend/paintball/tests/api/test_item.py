from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from paintball.models import (
    Brand,
    Category,
    Condition,
    Item,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class TestItemsAPI(APITestCase):

    def with_foreign_props(self, dict1):
        category = Category.objects.create(name="marker")
        brand = Brand.objects.create(name="planet eclipse")
        condition = Condition.objects.create(name="used")
        dict2 = {
            'category': category.id,
            'brand': brand.id,
            'condition': condition.id,
        }

        return {**dict1, **dict2}

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

    # POST
    def test_authenticated_user_create_item(self):
        """
        Ensure we can create items.
        """
        authenticated_user_token = self.create_user(False)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {authenticated_user_token}')
        response = self.client.post(
            '/api/items/',
            self.with_foreign_props({
                'title': 'test title',
                'sold': True,
                'description': 'test description',
                'year': 2010,
                'price': 1200.00,
            })
        )
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_user_not_create_item(self):
        """
        Ensure unauthenticated users can't create item.
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
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET
    def test_unauthenticated_user_get_items(self):
        """
        Ensure unauthenticated user can get items.
        """

        user = User.objects.create_user(
            'user@kingpaintball.com',
            'password'
        )

        category = Category.objects.create(name="marker")
        brand = Brand.objects.create(name="planet eclipse")
        condition = Condition.objects.create(name="used")

        Item.objects.create(
            title="title",
            sold=True,
            description="description",
            year=2010,
            price=199.99,
            user=user,
            category=category,
            brand=brand,
            condition=condition,
        )

        response = self.client.get('/api/items/1/', {}, format='json')

        self.assertDictContainsSubset({
            'id': 1,
            'title': 'title',
            'sold': True,
            'description': 'description',
            'year': 2010,
            'price': '199.99',
        }, response.data)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # PUT
    def test_update_item_belongs_to_user(self):
        """
        Ensure that only object owners can update the item.
        """
        # first create the item.
        authenticated_user_token = self.create_user(False)

        url = '/api/items/'
        data = self.with_foreign_props({
            'title': 'test title',
            'sold': True,
            'description': 'test description',
            'year': 2010,
            'price': 1200.00,
            'user': 1,
        })
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {authenticated_user_token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_data = data | {
            'title': 'new title',
            'sold': False,
            'description': 'new description',
            'year': 2020,
            'price': '130.00',
            'user': 1,
        }

        # update the item.
        new_response = self.client.put('/api/items/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({
            'id': 1,
            'title': new_data['title'],
            'sold': new_data['sold'],
            'description': new_data['description'],
            'year': new_data['year'],
            'price': new_data['price'],
        }, new_response.data)

    def test_update_item_not_belongs_to_user(self):
        """
        Ensure that only object owners can update the item.
        """
        # first create the item.
        user1_token = Token.objects.create(
            user=User.objects.create_user(
                'user@kingpaintball.com',
                'password'
            ))

        user2_token = Token.objects.create(
            user=User.objects.create_user(
                'user2@kingpaintball.com',
                'password'
            ))

        url = '/api/items/'
        data = self.with_foreign_props({
            'title': 'test title',
            'sold': True,
            'description': 'test description',
            'year': 2010,
            'price': 1200.00,
            'user': 1,
        })
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user1_token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_data = data | {
            'title': 'new title',
            'sold': False,
            'description': 'new description',
            'year': 2020,
            'price': '130.00',
            'user': 1,
        }

        # update the item.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
        new_response = self.client.put('/api/items/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_403_FORBIDDEN)

    # PATCH

    def test_patch_item_belongs_to_user(self):
        """
        Ensure that only object owners can patch the item.
        """
        # first create the item.
        authenticated_user_token = self.create_user(False)

        url = '/api/items/'
        data = self.with_foreign_props({
            'title': 'test title',
            'sold': True,
            'description': 'test description',
            'year': 2010,
            'price': 1200.00,
        })
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {authenticated_user_token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_data = data | {
            'year': 2020,
        }

        # update the item.
        new_response = self.client.patch('/api/items/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({
            'year': new_data['year'],
        }, new_response.data)

    def test_patch_item_not_belongs_to_user(self):
        """
        Ensure that non object owners can't update the item.
        """
        # first create the item.
        user1_token = Token.objects.create(
            user=User.objects.create_user(
                'user@kingpaintball.com',
                'password'
            ))

        user2_token = Token.objects.create(
            user=User.objects.create_user(
                'user2@kingpaintball.com',
                'password'
            ))

        url = '/api/items/'
        data = self.with_foreign_props({
            'title': 'test title',
            'sold': True,
            'description': 'test description',
            'year': 2010,
            'price': 1200.00,
        })
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user1_token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_data = data | {
            'year': 2020,
        }

        # update the item.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
        new_response = self.client.patch('/api/items/1/', new_data,)
        self.assertEqual(new_response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE

    def test_delete_item_belongs_to_user(self):
        """
        Ensure we can delete items.
        """

        user_token = self.create_user(False)

        data = self.with_foreign_props({
            'title': 'test title',
            'sold': True,
            'description': 'test description',
            'year': 2010,
            'price': 1200.00,
            'user': 1,
        })
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {user_token}')

        response = self.client.post('/api/items/', data, format='json')
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete('/api/items/1/',)

        # make sure there are 0 items.
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_item_not_belongs_to_user(self):
        """
        Ensure we can't delete items.
        """

        user1_token = Token.objects.create(
            user=User.objects.create_user(
                'user@kingpaintball.com',
                'password'
            ))

        user2_token = Token.objects.create(
            user=User.objects.create_user(
                'user2@kingpaintball.com',
                'password'
            ))

        data = self.with_foreign_props({
            'title': 'test title',
            'sold': True,
            'description': 'test description',
            'year': 2010,
            'price': 1200.00,
        })
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user1_token}')

        response = self.client.post('/api/items/', data, format='json')
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
        response = self.client.delete('/api/items/1/',)

        # make sure there are 0 items.
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
