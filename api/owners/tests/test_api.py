from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework import status

from api.tests.base import AuthenticatedAPITestCase
from api.owners.models import Owner

class OwnerAPITest(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.existing_owner = Owner.objects.create(
            name="Existing",
            cpf=22222222222,
            email="test2@email.com",
            phone_number=34987654320,
            address="RUA DO TESTE",
            address_2=123
        )

    def setUp(self):
        super().setUp()  # This authenticates as vet
        self.owner_data = {
            "name": "TEST NAME",
            "cpf": 11111111111,
            "email": "test@email.com",
            "phone_number": 34987654321,
            "address": "RUA DO TESTE",
            "address_2": 123
        }

    def test_create_owner(self):
        response = self.client.post(
            "/api/owners/",
            self.owner_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "TEST NAME")

    def test_list_owners(self):
        response = self.client.get("/api/owners/")

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_owner(self):
        response = self.client.get(
            f"/api/owners/{self.existing_owner.id}/"
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["name"], "Existing")

    def test_delete_name_false(self):
        self.authenticate_as_admin()  # Only admins can delete
        response = self.client.delete(
            f"/api/owners/{self.existing_owner.id}/"
        )

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_duplicate_cpf_fails(self):
        response = self.client.post(
            "/api/owners/",
            {
                "name": "Existing",
                "cpf": 22222222222
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)