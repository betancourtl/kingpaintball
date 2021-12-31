from django.test import TestCase
from paintball.models import (
    Image,
    Item,
    Brand,
    Category,
    Condition,
)
from django.contrib.auth import get_user_model
User = get_user_model()


class TestImageModel(TestCase):
    """ Test module for Image model """

    def test_create_image(self):
        """Test that an image gets created and that it belogs to item
        """
        category1 = Category.objects.create(name="marker")
        brand1 = Brand.objects.create(name="planet eclipse")
        condition1 = Condition.objects.create(name="used")
        user1 = User.objects.create(
            email="webdeveloperpr@gmail.com",
            password="123456",
            is_active=True
        )

        item1 = Item.objects.create(
            title='planet eclipse for sale',
            sold=True,
            description='Image in new in box conditions!',
            year=2000,
            price=200000.00,
            category=category1,
            brand=brand1,
            user=user1,
            condition=condition1,
        )

        image1 = Image.objects.create(
            image="my-image.jpg",
            item=item1
        )

        self.assertEqual(image1.image, 'my-image.jpg')
        self.assertEqual(image1.item_id, item1.id)
