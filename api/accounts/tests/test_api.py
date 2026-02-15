from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from api.accounts.models import Account

class TestAccountAPI(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "NEW USERNAME",
            "password": "PASSWORD",
            "first_name": "NAME",
            "last_name": "SURNAME",
            "license_number": "00000",
        }
        self.invalid_user_data = {
            "user_name": "INVALID USERNAME",
            "password": "PASSWORD",
            "full_name": "NAME",
            "license_number": "99999",
        }

        self.user = User.objects.create_user(
            username="USERNAME",
            first_name="NAME",
            last_name="SURNAME",
        )

        self.account = Account.objects.create(
            user=self.user,
            license_number="12345",
        )

    def test_register_account(self):
        response = self.client.post(
            "/api/accounts/",
            self.user_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "NEW USERNAME")

    def test_register_invalid_account(self):
        response = self.client.post(
            "/api/accounts/",
            self.invalid_user_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_account(self):
        response = self.client.get(
            f"/api/accounts/{self.account.pk}/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "USERNAME")

    def test_retrieve_invalid_account(self):
        response = self.client.get(
            f"/api/accounts/99/",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_accounts(self):
        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.client.post(
            "/api/accounts/",
            self.user_data,
            format="json"
        )

        response = self.client.get("/api/accounts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_account(self):
        new_account_data = {
            "username": "UPDATED USERNAME",
            "password": "PASSWORD",
            "first_name": "UPDATED NAME",
            "last_name": "UPDATED SURNAME",
            "license_number": "987654321",
        }

        response = self.client.put(
            f"/api/accounts/{self.account.pk}/",
            data=new_account_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "UPDATED USERNAME")
        self.assertEqual(response.data["first_name"], "UPDATED NAME")
        self.assertEqual(response.data["last_name"], "UPDATED SURNAME")
        self.assertEqual(response.data["license_number"], "987654321")

    def test_update_partial_account(self):
        new_account_data = {
            "username": "UPDATED USERNAME",
            "license_number": "987654321",
        }

        response = self.client.patch(
            f"/api/accounts/{self.account.pk}/",
            data=new_account_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "UPDATED USERNAME")
        self.assertEqual(response.data["first_name"], "NAME")
        self.assertEqual(response.data["last_name"], "SURNAME")
        self.assertEqual(response.data["license_number"], "987654321")

    def test_update_invalid_account(self):
        invalid_account_data = {
            "user_name": "INVALID",
            "pass_word": "INVALID",
            "firstname": "INVALID",
            "lastname": "INVALID",
            "licensenumber": "INVALID",
        }

        response = self.client.put(
            f"/api/accounts/{self.account.pk}/",
            data=invalid_account_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_partial_account_data = {
            "user_name": "UPDATED USERNAME",
            "licensenumber": "987654321",
        }

        response = self.client.patch(
            f"/api/accounts/{self.account.pk}/",
            data=invalid_partial_account_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account(self):
        response = self.client.delete(
            f"/api/accounts/{self.account.pk}/",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user = Account.objects.filter(pk=self.account.pk).get().user
        self.assertEqual(user.is_active, False)
