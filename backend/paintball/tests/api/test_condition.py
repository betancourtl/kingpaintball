from rest_framework import status
from rest_framework.test import APITestCase
from paintball.models import (
    Condition
)


class TestConditionAPI(APITestCase):

    def create_condition(self, condition_name):
        url = '/api/conditions/'
        data = {
            'name': condition_name
        }
        response = self.client.post(url, data)
        return response

    def test_create_condition(self):
        """
        Ensure we can create condition.
        """
        response = self.create_condition('new')
        self.assertEqual(Condition.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_condition(self):
        """
        Ensure we can get condition.
        """
        self.create_condition('new')

        url = '/api/conditions/1/'
        data = {'name': 'new'}
        response = self.client.get(url, data, format='json')
        self.assertDictContainsSubset({'id': 1, 'name': 'new'}, response.data)
        self.assertEqual(Condition.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_condition(self):
        """
        Ensure we can update condition.
        """
        self.create_condition('new')

        # Update the condition
        response = self.client.patch('/api/conditions/1/', {'name': 'used'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({'id': 1, 'name': 'used'}, response.data)

    def test_delete_condition(self):
        """
        Ensure we can get condition.
        """
        self.create_condition('new')

        # make sure there is only 1 item.
        self.assertEqual(Condition.objects.count(), 1)

        url = '/api/conditions/1/'
        response = self.client.delete(url)

        # make sure there are 0 items.
        self.assertEqual(Condition.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
