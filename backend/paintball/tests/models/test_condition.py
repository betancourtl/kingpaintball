from django.test import TestCase
from django.db.utils import IntegrityError
from paintball.models import Condition


class TestConditionModel(TestCase):
    """ Test module for Condition model """

    def test_condition_name(self):
        """Test that a condition gets created
        """
        condition1 = Condition.objects.create(name='new')
        condition2 = Condition.objects.create(name='used')

        self.assertEqual(condition1.name, 'new')
        self.assertEqual(condition2.name, 'used')

    def test_condition_name_unique(self):
        """Test that the condition is unique
        """
        try:
            Condition.objects.create(name='new')
            Condition.objects.create(name='new')
        except IntegrityError:
            return

        self.fail(
            'Something went wrong, IntegrityError should have been raised.'
        )
