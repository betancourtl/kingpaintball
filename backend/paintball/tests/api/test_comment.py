from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from paintball.models import (
    Brand,
    Category,
    Condition,
    Comment,
    User,
    Item,
)


class TestCommentsAPI(APITestCase):

    def create_item(self):
        category1 = Category.objects.create(name="marker")
        brand1 = Brand.objects.create(name="planet eclipse")
        condition1 = Condition.objects.create(name="used")
        user1 = User.objects.create(
            email="test@kingpaintball.com",
            username="test",
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

    # POST
    def test_authenticated_user_create_comment(self):
        """
        Ensure user can create comments.
        """
        user_token = self.create_user(False)
        item = self.create_item()
        data = {
            'comment': 'comment',
            'item': item.id
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
        response = self.client.post('/api/comments/', data)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_user_not_create_comment(self):
        """
        Ensure unauthenticated users can't create comment.
        """
        item = self.create_item()
        data = {
            'comment': 'comment',
            'item': item.id
        }

        response = self.client.post('/api/comments/', data)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET
    def test_unauthenticated_user_get_comments(self):
        """
        Ensure unauthenticated user can get comments.
        """

        item = self.create_item()
        data = {
            'comment': 'comment',
            'item': item.id
        }

        user_token = self.create_user(False)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
        response = self.client.post('/api/comments/', data)

        self.client.credentials()
        response = self.client.get('/api/comments/1/')

        self.assertDictContainsSubset({
            'comment': 'comment',
            'item': 1,
        }, response.data)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # PUT
    def test_update_comment_belongs_to_user(self):
        """
        Ensure that only object owners can update the comment.
        """
        user_token = self.create_user(False)
        item = self.create_item()
        data = {
            'comment': 'comment',
            'item': item.id
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
        self.client.post('/api/comments/', data)

        new_data = {
            'comment': 'new comment',
            'item': item.id,
        }

        # update the comment.
        new_response = self.client.put('/api/comments/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({
            'comment': new_data['comment'],
            'item': new_data['item'],
        }, new_response.data)

    def test_update_comment_not_belongs_to_user(self):
        """
        Ensure that only object owners can update the comment.
        """
        # first create the comment.
        user1 = User.objects.create_user(
            'user1',
            'user1@kingpaintball.com',
            'password'
        )

        user2 = User.objects.create_user(
            'user2',
            'user2@kingpaintball.com',
            'password'
        )

        user1_token = Token.objects.create(user=user1)
        user2_token = Token.objects.create(user=user2)

        item = self.create_item()
        data = {
            'comment': 'comment',
            'item': item.id
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user1_token}')
        self.client.post('/api/comments/', data)

        new_data = {
            'comment': 'new comment',
            'item': item.id,
        }

        # update the comment.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
        new_response = self.client.put('/api/comments/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_403_FORBIDDEN)

    # PATCH

    def test_patch_comment_belongs_to_user(self):
        """
        Ensure that only object owners can patch the comment.
        """
        # first create the comment.
        user1 = User.objects.create_user(
            'user1',
            'user1@kingpaintball.com',
            'password'
        )

        user1_token = Token.objects.create(user=user1)

        item = self.create_item()

        Comment.objects.create(
            comment='comment',
            item=item,
            user=user1
        )

        new_data = {
            'comment': 'new comment',
        }

        # update the comment.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user1_token}')
        new_response = self.client.patch('/api/comments/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({
            'comment': new_data['comment'],
            'item': 1
        }, new_response.data)

    def test_patch_comment_not_belongs_to_user(self):
        """
        Ensure that non object owners can't update the comment.
        """
        # first create the comment.
        user1 = User.objects.create_user(
            'user1',
            'user1@kingpaintball.com',
            'password'
        )

        user2 = User.objects.create_user(
            'user2',
            'user2@kingpaintball.com',
            'password'
        )

        user2_token = Token.objects.create(user=user2)

        item = self.create_item()

        Comment.objects.create(
            comment='comment',
            item=item,
            user=user1
        )

        new_data = {
            'comment': 'new comment',
        }

        # update the comment.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
        new_response = self.client.patch('/api/comments/1/', new_data,)

        self.assertEqual(new_response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE

    def test_delete_comment_belongs_to_user(self):
        """
        Ensure we can delete comments.
        """

        user1 = User.objects.create_user(
            'user1',
            'user1@kingpaintball.com',
            'password'
        )

        user1_token = Token.objects.create(user=user1)

        item = self.create_item()

        Comment.objects.create(
            comment='comment',
            item=item,
            user=user1
        )

        # update the comment.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user1_token}')
        new_response = self.client.delete('/api/comments/1/',)

        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(new_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_not_belongs_to_user(self):
        """
        Ensure we can't delete comments.
        """

        user1 = User.objects.create_user(
            'user1',
            'user1@kingpaintball.com',
            'password'
        )

        user2 = User.objects.create_user(
            'user2',
            'user2@kingpaintball.com',
            'password'
        )

        user2_token = Token.objects.create(user=user2)

        item = self.create_item()

        Comment.objects.create(
            comment='comment',
            item=item,
            user=user1
        )

        # update the comment.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
        new_response = self.client.delete('/api/comments/1/',)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(new_response.status_code, status.HTTP_403_FORBIDDEN)
