from django.contrib.auth.models import User
from rest_framework import status

from api.tests.base import AuthenticatedAPITestCase
from api.accounts.models import Account


class AccountPermissionTests(AuthenticatedAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_account = Account.objects.create(
            user=User.objects.create_user(
                username="testuser",
                password="testpass123",
                first_name="Test",
                last_name="User"
            ),
            license_number="TEST-123"
        )

    def setUp(self):
        super().setUp()
        self.new_user_data = {
            "username": "newuser",
            "password": "newpass123",
            "first_name": "New",
            "last_name": "User",
        }

    def test_unauthenticated_cannot_list_accounts(self):
        self.unauthenticate()
        response = self.client.get('/api/accounts/')
        self.assertUnauthorized(response)

    def test_unauthenticated_cannot_retrieve_account(self):
        self.unauthenticate()
        response = self.client.get(f'/api/accounts/{self.test_account.pk}/')
        self.assertUnauthorized(response)

    def test_unauthenticated_cannot_create_account(self):
        self.unauthenticate()
        response = self.client.post('/api/accounts/', self.new_user_data, format='json')
        self.assertUnauthorized(response)

    def test_regular_user_can_list_accounts(self):
        self.authenticate_as_regular()
        response = self.client.get('/api/accounts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_can_retrieve_account(self):
        self.authenticate_as_regular()
        response = self.client.get(f'/api/accounts/{self.test_account.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_create_account(self):
        self.authenticate_as_regular()
        response = self.client.post('/api/accounts/', self.new_user_data, format='json')
        self.assertForbidden(response)

    def test_regular_user_can_update_own_account(self):
        self.authenticate_as_regular()
        update_data = {
            "username": "regular",
            "password": "newpass",
            "first_name": "Updated",
            "last_name": "Regular",
        }
        response = self.client.patch(
            f'/api/accounts/{self.regular_account.pk}/',
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")

    def test_regular_user_cannot_update_others_account(self):
        self.authenticate_as_regular()
        update_data = {
            "username": "testuser",
            "first_name": "Hacked",
        }
        response = self.client.patch(
            f'/api/accounts/{self.test_account.pk}/',
            update_data,
            format='json'
        )
        self.assertForbidden(response)

    def test_regular_user_cannot_promote_self_to_vet(self):
        self.authenticate_as_regular()
        update_data = {
            "username": "regular",
            "license_number": "HACKED-123",
        }
        response = self.client.patch(
            f'/api/accounts/{self.regular_account.pk}/',
            update_data,
            format='json'
        )
        if response.status_code == status.HTTP_200_OK:
            self.assertIsNone(response.data.get("license_number"))

    def test_vet_can_list_accounts(self):
        self.authenticate_as_vet()
        response = self.client.get('/api/accounts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vet_can_retrieve_account(self):
        self.authenticate_as_vet()
        response = self.client.get(f'/api/accounts/{self.test_account.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vet_cannot_create_account(self):
        self.authenticate_as_vet()
        response = self.client.post('/api/accounts/', self.new_user_data, format='json')
        self.assertForbidden(response)

    def test_vet_can_update_own_account(self):
        self.authenticate_as_vet()
        update_data = {
            "username": "vet",
            "first_name": "Updated",
            "last_name": "Vet",
        }
        response = self.client.patch(
            f'/api/accounts/{self.vet_account.pk}/',
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")

    def test_vet_cannot_update_others_account(self):
        self.authenticate_as_vet()
        update_data = {
            "username": "testuser",
            "first_name": "Hacked",
        }
        response = self.client.patch(
            f'/api/accounts/{self.test_account.pk}/',
            update_data,
            format='json'
        )
        self.assertForbidden(response)

    def test_admin_can_create_account(self):
        self.authenticate_as_admin()
        response = self.client.post('/api/accounts/', self.new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")

    def test_admin_can_update_any_account(self):
        self.authenticate_as_admin()
        update_data = {
            "username": "testuser",
            "first_name": "Admin Updated",
        }
        response = self.client.patch(
            f'/api/accounts/{self.test_account.pk}/',
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Admin Updated")

    def test_admin_can_delete_account(self):
        self.authenticate_as_admin()

        response = self.client.delete(f'/api/accounts/{self.test_account.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user = User.objects.get(pk=self.test_account.user.pk)

        self.assertFalse(user.is_active)

    def test_regular_user_cannot_delete_account(self):
        self.authenticate_as_regular()

        response = self.client.delete(f'/api/accounts/{self.test_account.pk}/')

        self.assertForbidden(response)

    def test_vet_cannot_delete_account(self):
        self.authenticate_as_vet()

        response = self.client.delete(f'/api/accounts/{self.test_account.pk}/')

        self.assertForbidden(response)

