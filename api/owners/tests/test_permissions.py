from rest_framework import status

from api.tests.base import AuthenticatedAPITestCase
from api.owners.models import Owner


class OwnerPermissionTests(AuthenticatedAPITestCase):
    """Test Owner access control and permissions"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.owner = Owner.objects.create(
            name="Test Owner",
            cpf=12345678901,
            email="owner@test.com",
            phone_number=11987654321,
            address="Test Street",
            address_2=100
        )

    def setUp(self):
        super().setUp()
        self.owner_data = {
            "name": "New Owner",
            "cpf": 98765432109,
            "email": "newowner@test.com",
            "phone_number": 11912345678,
            "address": "New Street",
            "address_2": 200
        }

    def test_unauthenticated_cannot_access(self):
        """Unauthenticated users should get 401"""
        self.unauthenticate()
        response = self.client.get('/api/owners/')
        self.assertUnauthorized(response)

    def test_regular_user_can_create(self):
        """Regular users can create owners"""
        self.authenticate_as_regular()
        response = self.client.post('/api/owners/', self.owner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_can_update(self):
        """Regular users can update owners"""
        self.authenticate_as_regular()
        update_data = {
            "name": "Updated Owner",
            "cpf": 12345678901,
            "email": "updated@test.com",
            "phone_number": 11987654321,
            "address": "Updated Street",
            "address_2": 100
        }
        response = self.client.put(f'/api/owners/{self.owner.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_delete(self):
        """Regular users cannot delete owners"""
        self.authenticate_as_regular()
        response = self.client.delete(f'/api/owners/{self.owner.id}/')
        self.assertForbidden(response)

    def test_vet_can_create(self):
        """Vets can create owners"""
        self.authenticate_as_vet()
        response = self.client.post('/api/owners/', self.owner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vet_can_update(self):
        """Vets can update owners"""
        self.authenticate_as_vet()
        update_data = {
            "name": "Vet Updated",
            "cpf": 12345678901,
            "email": "vet@test.com",
            "phone_number": 11987654321,
            "address": "Vet Street",
            "address_2": 100
        }
        response = self.client.put(f'/api/owners/{self.owner.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vet_cannot_delete(self):
        """Vets cannot delete owners"""
        self.authenticate_as_vet()
        response = self.client.delete(f'/api/owners/{self.owner.id}/')
        self.assertForbidden(response)

    def test_admin_can_delete(self):
        """Admins can delete owners"""
        self.authenticate_as_admin()
        response = self.client.delete(f'/api/owners/{self.owner.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
