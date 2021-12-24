from django.test import TestCase
from user.models import Account
from django.contrib.auth import get_account_model

User = get_account_model()


class TestAccountAPI(TestCase):

    # POST
    def test_create_account(self):
        "Create user"
        pass

    # GET
    def test_get_account(self):
        "Get user"
        pass

    # PATH
    def test_patch_account(self):
        "Get user"
        pass

    # PUT
    def test_update_account(self):
        "Put user"
        pass

    # DELETE
    def test_delete_account(self):
        "Delete user"
        pass
