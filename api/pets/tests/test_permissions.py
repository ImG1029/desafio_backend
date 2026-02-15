from rest_framework import status

from api.tests.base import AuthenticatedAPITestCase
from api.owners.models import Owner
from api.pets.models import Pet


class PetPermissionTests(AuthenticatedAPITestCase):
    """Test Pet access control and permissions"""

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
        cls.pet = Pet.objects.create(
            name="Test Pet",
            species="Dog",
            breed="Labrador",
            birth_date="2020-01-01",
            owner=cls.owner
        )

    def setUp(self):
        super().setUp()
        self.pet_data = {
            "name": "New Pet",
            "species": "Cat",
            "breed": "Persian",
            "birth_date": "2021-05-15",
            "owner": self.owner.id
        }

    def test_unauthenticated_cannot_access(self):
        """Unauthenticated users should get 401"""
        self.unauthenticate()
        response = self.client.get('/api/pets/')
        self.assertUnauthorized(response)

    def test_regular_user_can_create(self):
        """Regular users can create pets"""
        self.authenticate_as_regular()
        response = self.client.post('/api/pets/', self.pet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_can_update(self):
        """Regular users can update pets"""
        self.authenticate_as_regular()
        update_data = {
            "name": "Updated Pet",
            "species": "Dog",
            "breed": "Labrador",
            "birth_date": "2020-01-01",
            "owner": self.owner.id
        }
        response = self.client.put(f'/api/pets/{self.pet.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_delete(self):
        """Regular users cannot delete pets"""
        self.authenticate_as_regular()
        response = self.client.delete(f'/api/pets/{self.pet.id}/')
        self.assertForbidden(response)

    def test_vet_can_create(self):
        """Vets can create pets"""
        self.authenticate_as_vet()
        response = self.client.post('/api/pets/', self.pet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vet_can_update(self):
        """Vets can update pets"""
        self.authenticate_as_vet()
        update_data = {
            "name": "Vet Updated Pet",
            "species": "Dog",
            "breed": "Labrador",
            "birth_date": "2020-01-01",
            "owner": self.owner.id
        }
        response = self.client.put(f'/api/pets/{self.pet.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vet_cannot_delete(self):
        """Vets cannot delete pets"""
        self.authenticate_as_vet()
        response = self.client.delete(f'/api/pets/{self.pet.id}/')
        self.assertForbidden(response)

    def test_admin_can_delete(self):
        """Admins can delete pets"""
        self.authenticate_as_admin()
        response = self.client.delete(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
