from paintball.models import Brand
from django.test import TestCase
from django.db.utils import IntegrityError


class TestBrandModel(TestCase):
    """ Test module for Brand model """

    def test_brand_name(self):
        """Test that a brand gets created
        """
        brand1 = Brand.objects.create(name='dye')
        brand2 = Brand.objects.create(name='eclipse')

        self.assertEqual(brand1.name, 'dye')
        self.assertEqual(brand2.name, 'eclipse')

    def test_brand_name_unique(self):
        """Test that the brand is unique
        """
        try:
            Brand.objects.create(name='dye')
            Brand.objects.create(name='dye')
        except IntegrityError:
            return

        self.fail(
            'Something went wrong, IntegrityError should have been raised.'
        )
