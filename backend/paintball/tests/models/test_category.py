from django.test import TestCase
from django.db.utils import IntegrityError
from paintball.models import Category


class TestCategoryModel(TestCase):
    """ Test module for Category model """

    def test_category_name(self):
        """Test that a category gets created
        """
        category1 = Category.objects.create(name='marker')
        category2 = Category.objects.create(name='jerseys')

        self.assertEqual(category1.name, 'marker')
        self.assertEqual(category2.name, 'jerseys')

    def test_category_name_unique(self):
        """Test that the category is unique
        """
        try:
            Category.objects.create(name='marker')
            Category.objects.create(name='marker')
        except IntegrityError:
            return

        self.fail(
            'Something went wrong, IntegrityError should have been raised.'
        )
