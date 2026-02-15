from django.contrib.auth.models import User
from rest_framework import status

from api.tests.base import AuthenticatedAPITestCase
from api.accounts.models import Account

class TestAccountAPI(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # Create an additional account for testing
        cls.test_user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        cls.test_account = Account.objects.create(
            user=cls.test_user,
            license_number="54321",
        )

    def setUp(self):
        super().setUp()  # This authenticates as vet
        self.user_data = {
            "username": "NEW USERNAME",
            "password": "PASSWORD",
            "first_name": "NAME",
            "last_name": "SURNAME",
        }
        self.invalid_user_data = {
            "user_name": "INVALID USERNAME",
            "password": "PASSWORD",
            "full_name": "NAME",
        }


    def test_register_account(self):
        self.authenticate_as_admin()  # Only admins can create accounts
        response = self.client.post(
            "/api/accounts/",
            self.user_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "NEW USERNAME")

    def test_register_invalid_account(self):
        self.authenticate_as_admin()  # Only admins can create accounts
        response = self.client.post(
            "/api/accounts/",
            self.invalid_user_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_account(self):
        response = self.client.get(
            f"/api/accounts/{self.test_account.pk}/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_retrieve_invalid_account(self):
        response = self.client.get(
            f"/api/accounts/99/",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_accounts(self):
        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # We have admin, vet, regular, and test_account (4 accounts)
        self.assertEqual(len(response.data), 4)

        self.authenticate_as_admin()  # Only admins can create accounts
        self.client.post(
            "/api/accounts/",
            self.user_data,
            format="json"
        )

        response = self.client.get("/api/accounts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_update_account(self):
        new_account_data = {
            "username": "UPDATED USERNAME",
            "password": "PASSWORD",
            "first_name": "UPDATED NAME",
            "last_name": "UPDATED SURNAME"
        }

        response = self.client.put(
            f"/api/accounts/{self.vet_account.pk}/",
            data=new_account_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "UPDATED USERNAME")
        self.assertEqual(response.data["first_name"], "UPDATED NAME")
        self.assertEqual(response.data["last_name"], "UPDATED SURNAME")

    def test_update_partial_account(self):
        new_account_data = {
            "username": "UPDATED USERNAME",
        }

        # Update vet's own account
        response = self.client.patch(
            f"/api/accounts/{self.vet_account.pk}/",
            data=new_account_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "UPDATED USERNAME")
        self.assertEqual(response.data["first_name"], "Vet")
        self.assertEqual(response.data["last_name"], "Doctor")

    def test_update_invalid_account(self):
        invalid_account_data = {
            "user_name": "INVALID",
            "pass_word": "INVALID",
            "firstname": "INVALID",
            "lastname": "INVALID",
        }

        # Test updating own account with invalid data
        response = self.client.put(
            f"/api/accounts/{self.vet_account.pk}/",
            data=invalid_account_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_partial_account_data = {
            "user_name": "UPDATED USERNAME",
        }

        response = self.client.patch(
            f"/api/accounts/{self.vet_account.pk}/",
            data=invalid_partial_account_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account(self):
        self.authenticate_as_admin()  # Only admins can delete accounts
        response = self.client.delete(
            f"/api/accounts/{self.test_account.pk}/",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user = Account.objects.filter(pk=self.test_account.pk).get().user
        self.assertEqual(user.is_active, False)
