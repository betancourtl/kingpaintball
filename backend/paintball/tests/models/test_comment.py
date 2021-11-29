from django.test import TestCase
from django.db.utils import IntegrityError
from django.test.utils import setup_databases
from user.models import (
    User,
)
from paintball.models import (
    Item,
    Brand,
    Comment,
    Category,
    Condition,
)


class TestCommentModel(TestCase):
    """ Test module for Comment model """

    def test_comment(self):
        """Test that an comment gets created and that it belogs to item
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
            description='Comment in new in box conditions!',
            year=2000,
            price=200000.00,
            category=category1,
            brand=brand1,
            user=user1,
            condition=condition1,
        )

        comment1 = Comment.objects.create(
            comment="comment1",
            item=item1,
            user=user1
        )

        comment2 = Comment.objects.create(
            comment="comment2",
            item=item1,
            user=user1
        )

        self.assertEqual(comment1.comment, 'comment1')
        self.assertEqual(comment1.item, item1)
        self.assertEqual(comment1.user, user1)

        self.assertEqual(comment2.comment, 'comment2')
        self.assertEqual(comment2.item, item1)
        self.assertEqual(comment2.user, user1)
