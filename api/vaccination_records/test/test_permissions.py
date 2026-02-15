from django.contrib.auth.models import User
from rest_framework import status

from api.tests.base import AuthenticatedAPITestCase
from api.accounts.models import Account
from api.owners.models import Owner
from api.pets.models import Pet
from api.vaccines.models import Vaccine
from api.vaccination_records.models import VaccinationRecord


class VaccinationRecordPermissionTests(AuthenticatedAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.vet2_user = User.objects.create_user(
            username="vet2",
            password="vet2123",
            first_name="Second",
            last_name="Vet"
        )
        cls.vet2_account = Account.objects.create(
            user=cls.vet2_user,
            license_number="VET-67890"
        )
        
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
        
        cls.vaccine = Vaccine.objects.create(
            name="Rabies",
            type="Viral",
            manufacturer="Test Pharma",
            recommended_interval_days=365
        )

        cls.record = VaccinationRecord.objects.create(
            pet=cls.pet,
            vaccine=cls.vaccine,
            veterinarian=cls.vet_account
        )

        cls.record2 = VaccinationRecord.objects.create(
            pet=cls.pet,
            vaccine=cls.vaccine,
            veterinarian=cls.vet2_account
        )

    def setUp(self):
        super().setUp()
        self.record_data = {
            "pet": self.pet.id,
            "vaccine": self.vaccine.id,
            "veterinarian": self.vet_account.id,
        }

    def test_unauthenticated_cannot_access(self):
        self.unauthenticate()

        response = self.client.get('/api/vaccination-records/')

        self.assertUnauthorized(response)

    def test_regular_user_can_read(self):
        self.authenticate_as_regular()

        response = self.client.get('/api/vaccination-records/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_create(self):
        self.authenticate_as_regular()

        response = self.client.post('/api/vaccination-records/', self.record_data, format='json')

        self.assertForbidden(response)

    def test_regular_user_cannot_update(self):
        self.authenticate_as_regular()

        update_data = {"next_dose_recommendation": "2026-01-01"}
        response = self.client.patch(f'/api/vaccination-records/{self.record.id}/', update_data, format='json')

        self.assertForbidden(response)

    def test_vet_can_create_record(self):
        self.authenticate_as_vet()

        response = self.client.post('/api/vaccination-records/', self.record_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vet_can_update_own_record(self):
        self.authenticate_as_vet()

        update_data = {"next_dose_recommendation": "2026-12-31"}
        response = self.client.patch(f'/api/vaccination-records/{self.record.id}/', update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vet_cannot_update_others_record(self):
        self.authenticate_as_vet()

        update_data = {"next_dose_recommendation": "2026-12-31"}
        response = self.client.patch(f'/api/vaccination-records/{self.record2.id}/', update_data, format='json')

        self.assertForbidden(response)

    def test_vet_cannot_delete(self):
        self.authenticate_as_vet()

        response = self.client.delete(f'/api/vaccination-records/{self.record.id}/')

        self.assertForbidden(response)

    def test_admin_can_update_any_record(self):
        self.authenticate_as_admin()

        update_data = {"next_dose_recommendation": "2027-01-01"}
        response = self.client.patch(f'/api/vaccination-records/{self.record.id}/', update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_record(self):
        self.authenticate_as_admin()

        response = self.client.delete(f'/api/vaccination-records/{self.record.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
