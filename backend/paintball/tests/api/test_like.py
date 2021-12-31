from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from paintball.models import (
    Brand,
    Category,
    Condition,
    Like,
    Item,
)
from django.contrib.auth import get_user_model
User = get_user_model()



class TestLikesAPI(APITestCase):

    def create_item(self):
        category1 = Category.objects.create(name="marker")
        brand1 = Brand.objects.create(name="planet eclipse")
        condition1 = Condition.objects.create(name="used")
        user1 = User.objects.create(
            email="test@kingpaintball.com",
            password="password",
            is_active=True
        )

        item = Item.objects.create(
            title='title',
            sold=True,
            description='description',
            year=2000,
            price=100.00,
            category=category1,
            brand=brand1,
            user=user1,
            condition=condition1,
        )

        return item

    # POST
    def test_authenticated_user_create_like(self):
        """
        Ensure user can create likes.
        """

        item = self.create_item()
        self.assertEqual(Item.objects.count(), 1)

        user = User.objects.create_user(
            'user@kingpaintball.com',
            'password'
        )

        user_token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')

        response = self.client.post(
            '/api/likes/', {
                'item': item.id
            })

        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_unauthenticated_user_not_create_like(self):
        """
        Ensure unauthenticated users can't create like.
        """
        item = self.create_item()
        data = {
            'item': item.id
        }

        response = self.client.post('/api/likes/', data)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET
    def test_unauthenticated_user_get_likes(self):
        """
        Ensure unauthenticated user can get likes.
        """

        item = self.create_item()
        data = {
            'item': item.id
        }

        user = User.objects.create_user(
            'user@kingpaintball.com',
            'password'
        )

        user_token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
        response = self.client.post('/api/likes/', data)

        self.client.credentials()
        response = self.client.get('/api/likes/1/')

        self.assertDictContainsSubset({
            'item': 1,
        }, response.data)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # PUT
    def test_update_like_belongs_to_user(self):
        """
        Ensure that only object owners can update the like.
        """
        user = User.objects.create_user(
            'user@kingpaintball.com',
            'password'
        )

        user_token = Token.objects.create(user=user)

        item = self.create_item()
        data = {
            'item': item.id
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
        self.client.post('/api/likes/', data)

        new_data = {
            'item': item.id,
        }

        # update the like.
        new_response = self.client.put('/api/likes/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_like_not_belongs_to_user(self):
        """
        Ensure that only object owners can update the like.
        """
        # first create the like.
        user1 = User.objects.create_user(
            'user1@kingpaintball.com',
            'password'
        )

        user2 = User.objects.create_user(
            'user2@kingpaintball.com',
            'password'
        )

        user1_token = Token.objects.create(user=user1)
        user2_token = Token.objects.create(user=user2)

        item = self.create_item()
        data = {
            'item': item.id
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user1_token}')
        self.client.post('/api/likes/', data)

        new_data = {
            'item': item.id,
        }

        # update the like.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
        new_response = self.client.put('/api/likes/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PATCH

    def test_patch_like_belongs_to_user(self):
        """
        Ensure that only object owners can patch the like.
        """
        # first create the like.
        user1 = User.objects.create_user(
            'user1@kingpaintball.com',
            'password'
        )

        user1_token = Token.objects.create(user=user1)

        item = self.create_item()

        Like.objects.create(
            item=item,
            user=user1
        )

        new_data = {
            'like': 'new like',
        }

        # update the like.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user1_token}')
        new_response = self.client.patch('/api/likes/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_like_not_belongs_to_user(self):
        """
        Ensure that non object owners can't update the like.
        """
        # first create the like.
        user1 = User.objects.create_user(
            'user1@kingpaintball.com',
            'password'
        )

        user2 = User.objects.create_user(
            'user2@kingpaintball.com',
            'password'
        )

        user2_token = Token.objects.create(user=user2)

        item = self.create_item()

        Like.objects.create(
            item=item,
            user=user1
        )

        new_data = {
            'like': 'new like',
        }

        # update the like.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
        new_response = self.client.patch('/api/likes/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE

    def test_delete_like_belongs_to_user(self):
        """
        Ensure we can delete likes.
        """

        user1 = User.objects.create_user(
            'user1@kingpaintball.com',
            'password'
        )

        user1_token = Token.objects.create(user=user1)

        item = self.create_item()

        Like.objects.create(
            item=item,
            user=user1
        )

        # update the like.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user1_token}')
        new_response = self.client.delete('/api/likes/1/',)

        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(new_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_like_not_belongs_to_user(self):
        """
        Ensure we can't delete likes.
        """

        user1 = User.objects.create_user(
            'user1@kingpaintball.com',
            'password'
        )

        user2 = User.objects.create_user(
            'user2@kingpaintball.com',
            'password'
        )

        user2_token = Token.objects.create(user=user2)

        item = self.create_item()

        Like.objects.create(
            item=item,
            user=user1
        )

        # update the like.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
        new_response = self.client.delete('/api/likes/1/',)

        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(new_response.status_code, status.HTTP_403_FORBIDDEN)
