from django.test import TestCase
from django.db.utils import IntegrityError
from django.test.utils import setup_databases
from core.models import (
    User,
)
from paintball.models import (
    Item,
    Brand,
    Category,
    Condition,
)


class TestItemModel(TestCase):
    """ Test module for Item model """

    def test_item_title(self):
        """Test that a item gets created
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
            description='Item in new in box conditions!',
            year=2000,
            price=200000.00,
            category=category1,
            brand=brand1,
            user=user1,
            condition=condition1,
        )

        self.assertEqual(item1.title, 'planet eclipse for sale')
        self.assertEqual(item1.sold, True)
        self.assertEqual(item1.description, 'Item in new in box conditions!')
        self.assertEqual(item1.year, 2000)
        self.assertEqual(item1.price, 200000.00)
        self.assertEqual(item1.category, category1)
        self.assertEqual(item1.brand, brand1)
        self.assertEqual(item1.user, user1)
        self.assertEqual(item1.condition, condition1)
