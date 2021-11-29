from django.test import TestCase
from django.db.utils import IntegrityError
from django.test.utils import setup_databases
from user.models import (
    User,
)
from paintball.models import (
    Item,
    Like,
    Item,
    Brand,
    Category,
    Condition,
)


class TestLikeModel(TestCase):
    """ Test module for Like model """

    def test_like(self):
        """Test that an like gets created and that it belogs to item
        """
        category1 = Category.objects.create(name="marker")
        brand1 = Brand.objects.create(name="planet eclipse")
        condition1 = Condition.objects.create(name="used")
        user1 = User.objects.create(
            email="webdeveloperpr@gmail.com",
            name="user",
            password="123456",
            is_active=True
        )

        item1 = Item.objects.create(
            title='planet eclipse for sale',
            sold=True,
            description='Like in new in box conditions!',
            year=2000,
            price=200000.00,
            category=category1,
            brand=brand1,
            user=user1,
            condition=condition1,
        )

        like1 = Like.objects.create(
            user=user1,
            item=item1
        )
        self.assertEqual(like1.user, user1)
        self.assertEqual(like1.item, item1)
