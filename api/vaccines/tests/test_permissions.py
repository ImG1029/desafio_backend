from rest_framework import status

from api.tests.base import AuthenticatedAPITestCase
from api.vaccines.models import Vaccine


class VaccinePermissionTests(AuthenticatedAPITestCase):
    """Test Vaccine access control and permissions"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.vaccine = Vaccine.objects.create(
            name="Test Vaccine",
            type="Type A",
            manufacturer="Test Pharma",
            recommended_interval_days=365
        )

    def setUp(self):
        super().setUp()
        self.vaccine_data = {
            "name": "New Vaccine",
            "type": "Type B",
            "manufacturer": "New Pharma",
            "recommended_interval_days": 180
        }

    def test_unauthenticated_cannot_access(self):
        """Unauthenticated users should get 401"""
        self.unauthenticate()
        response = self.client.get('/api/vaccines/')
        self.assertUnauthorized(response)

    def test_regular_user_can_read(self):
        """Regular users can only read vaccines"""
        self.authenticate_as_regular()
        response = self.client.get('/api/vaccines/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_create(self):
        """Regular users cannot create vaccines"""
        self.authenticate_as_regular()
        response = self.client.post('/api/vaccines/', self.vaccine_data, format='json')
        self.assertForbidden(response)

    def test_regular_user_cannot_update(self):
        """Regular users cannot update vaccines"""
        self.authenticate_as_regular()
        update_data = {"name": "Updated Vaccine"}
        response = self.client.patch(f'/api/vaccines/{self.vaccine.id}/', update_data, format='json')
        self.assertForbidden(response)

    def test_regular_user_cannot_delete(self):
        """Regular users cannot delete vaccines"""
        self.authenticate_as_regular()
        response = self.client.delete(f'/api/vaccines/{self.vaccine.id}/')
        self.assertForbidden(response)

    def test_vet_can_create(self):
        """Vets can create vaccines"""
        self.authenticate_as_vet()
        response = self.client.post('/api/vaccines/', self.vaccine_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vet_can_update(self):
        """Vets can update vaccines"""
        self.authenticate_as_vet()
        update_data = {"name": "Vet Updated Vaccine"}
        response = self.client.patch(f'/api/vaccines/{self.vaccine.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vet_cannot_delete(self):
        """Vets cannot delete vaccines"""
        self.authenticate_as_vet()
        response = self.client.delete(f'/api/vaccines/{self.vaccine.id}/')
        self.assertForbidden(response)

    def test_admin_can_delete(self):
        """Admins can delete vaccines"""
        self.authenticate_as_admin()
        response = self.client.delete(f'/api/vaccines/{self.vaccine.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
