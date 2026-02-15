from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from api.accounts.models import Account

class TestAccountModel(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="USERNAME",
            first_name="NAME",
            last_name="SURNAME",
        )

        self.account = Account.objects.create(
            user=self.user,
            license_number="12345",
        )

    def test_accounts_creation(self):
        self.assertEqual(self.account.user.username, "USERNAME")
        self.assertEqual(self.account.user.first_name, "NAME")
        self.assertEqual(self.account.user.last_name, "SURNAME")
        self.assertEqual(self.account.license_number, "12345")
