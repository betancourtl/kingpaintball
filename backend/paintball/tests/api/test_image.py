import tempfile
from PIL import Image as PilImage
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from paintball.models import (
    Brand,
    Category,
    Condition,
    User,
    Item,
    Image,
)
from django.test import override_settings
import shutil

TEST_DIR = 'test_data'


class TestImagesAPI(APITestCase):
    @classmethod
    def tearDownClass(cls):
        print("\nDeleting temporary files...\n")

        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

    def create_item(self, user=None):
        category1 = Category.objects.create(name="marker")
        brand1 = Brand.objects.create(name="planet eclipse")
        condition1 = Condition.objects.create(name="used")
        user1 = user or User.objects.create(
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

    # POST
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_authenticated_item_owner_create_image(self):
        """
        Ensure user can create images.
        """
        user = User.objects.create_user(
            'user',
            'user@kingpaintball.com',
            'password'
        )

        user_token = Token.objects.create(user=user)

        item = self.create_item(user)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = PilImage.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            data = {
                'image': ntf,
                'item': item.id
            }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
            response = self.client.post(
                '/api/images/',
                data,
                format='multipart'
            )

        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_authenticated_non_item_owner_create_image(self):
        """
        Ensure users who don't own an item can't create an image
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

        user1_token = Token.objects.create(user=user1)
        user2_token = Token.objects.create(user=user2)

        item = self.create_item(user1)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = PilImage.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            data = {
                'image': ntf,
                'item': item.id
            }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
            response = self.client.post(
                '/api/images/',
                data,
                format='multipart'
            )

        self.assertEqual(Image.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_unauthenticated_user_not_create_image(self):
        """
        Ensure unauthenticated users can't create image.
        """

        item = self.create_item()

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = PilImage.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            data = {
                'image': ntf,
                'item': item.id
            }

            response = self.client.post(
                '/api/images/',
                data,
                format='multipart'
            )

        self.assertEqual(Image.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_unauthenticated_user_get_images(self):
        """
        Ensure unauthenticated user can get images.
        """

        user = User.objects.create_user(
            'user',
            'user@kingpaintball.com',
            'password'
        )

        user_token = Token.objects.create(user=user)

        item = self.create_item(user)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = PilImage.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            data = {
                'image': ntf,
                'item': item.id
            }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
            response = self.client.post(
                '/api/images/',
                data,
                format='multipart'
            )

        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.credentials()
        response2 = self.client.get('/api/images/1/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    # PUT

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_update_image_belongs_to_user(self):
        """
        Ensure that only object owners can update the image.
        """
        user = User.objects.create_user(
            'user',
            'user@kingpaintball.com',
            'password'
        )

        user_token = Token.objects.create(user=user)

        item = self.create_item(user)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = PilImage.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            data = {
                'image': ntf,
                'item': item.id
            }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
            response = self.client.post(
                '/api/images/',
                data,
                format='multipart'
            )

        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = PilImage.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            data = {
                'image': ntf,
                'item': item.id
            }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
            response = self.client.put(
                '/api/images/1/',
                data,
                format='multipart'
            )
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    # PATCH
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_patch_image_belongs_to_user(self):
        """
        Ensure that only object owners can patch the image.
        """
        user = User.objects.create_user(
            'user',
            'user@kingpaintball.com',
            'password'
        )

        user_token = Token.objects.create(user=user)

        item = self.create_item(user)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = PilImage.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            data = {
                'image': ntf,
                'item': item.id
            }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
            response = self.client.post(
                '/api/images/',
                data,
                format='multipart'
            )

        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = PilImage.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            data = {
                'image': ntf,
            }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
            response = self.client.patch(
                '/api/images/1/',
                data,
                format='multipart'
            )
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_delete_image_belongs_to_user(self):
        """
        Ensure item owner can delete item images.
        """

        user = User.objects.create_user(
            'user',
            'user@kingpaintball.com',
            'password'
        )

        user_token = Token.objects.create(user=user)

        item = self.create_item(user)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = PilImage.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            data = {
                'image': ntf,
                'item': item.id
            }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
            response = self.client.post(
                '/api/images/',
                data,
                format='multipart'
            )

        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete('/api/images/1/')

        self.assertEqual(Image.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_delete_image_not_belongs_to_user(self):
        """
        Ensure non item owner can't delete images.
        """

        user1 = User.objects.create_user(
            'user1',
            'user1@kingpaintball.com',
            'password'
        )

        user2 = User.objects.create_user(
            'user2',
            'user@kingpaintball.com',
            'password'
        )

        user1_token = Token.objects.create(user=user1)
        user2_token = Token.objects.create(user=user2)

        item = self.create_item(user1)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = PilImage.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            data = {
                'image': ntf,
                'item': item.id
            }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user1_token}')
            response = self.client.post(
                '/api/images/',
                data,
                format='multipart'
            )

        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user2_token}')
        response = self.client.delete('/api/images/1/')

        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
