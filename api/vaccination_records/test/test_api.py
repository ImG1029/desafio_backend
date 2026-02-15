from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from api.accounts.models import Account
from api.pets.models import Pet
from api.owners.models import Owner
from api.vaccines.models import Vaccine
from api.vaccination_records.models import VaccinationRecord


class TestVaccinationRecordAPI(APITestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            name="FRANKLIN",
            cpf=11111111111,
            email="test@email.com",
            phone_number=34987654321,
            address="RUA DO TESTE",
            address_2=123,
        )

        self.pet = Pet.objects.create(
            name="CHOP",
            species="DOG",
            breed="ROTTWEILER",
            birth_date="2000-12-31",
            owner_id=self.owner.pk,
        )

        self.vaccine = Vaccine.objects.create(
            name="VACCINE NAME",
            type="VACCINE TYPE",
            manufacturer="VACCINE MANUFACTURER",
            recommended_interval_days=365,
        )

        self.vaccine_rabies = Vaccine.objects.create(
            name="RABIES",
            type="RABIES TYPE",
            manufacturer="FAMOUS MANUFACTURER",
            recommended_interval_days=365,
        )

        self.user = User.objects.create_user(
            username="VET USERNAME",
            first_name="VET NAME",
            last_name="VET SURNAME",
        )

        self.account = Account.objects.create(
            user=self.user,
            license_number="12345",
        )

        self.record = VaccinationRecord.objects.create(
            pet=self.pet,
            vaccine=self.vaccine,
            veterinarian=self.account,
        )

        self.record_data = {
            "pet": self.pet.pk,
            "vaccine": self.vaccine_rabies.pk,
            "veterinarian": self.account.pk,
        }

        self.invalid_record_data = {
            "pet": 999,
            "vaccine": 999,
            "vet": 999,
        }

    def test_create_record(self):
        response = self.client.post(
            '/api/vaccination-records/',
            self.record_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["pet"]["name"], "CHOP")
        self.assertEqual(response.data["vaccine"]["name"], "RABIES")
        self.assertEqual(response.data["veterinarian"]["username"], "VET USERNAME")
        self.assertIsNotNone(response.data["vaccinated_at"])

        record = VaccinationRecord.objects.get(id=response.data["id"])
        expected_date = record.vaccinated_at.date() + timedelta(days=365)
        self.assertIsNotNone(response.data["next_dose_recommendation"])
        self.assertEqual(record.next_dose_recommendation, expected_date)

    def test_create_invalid_record(self):
        response = self.client.post(
            '/api/vaccination-records/',
            self.invalid_record_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_record(self):
        response = self.client.get(
            f'/api/vaccination-records/{self.record.pk}/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pet"]["name"], "CHOP")
        self.assertEqual(response.data["vaccine"]["name"], "VACCINE NAME")
        self.assertEqual(response.data["veterinarian"]["username"], "VET USERNAME")

    def test_retrieve_invalid_record(self):
        response = self.client.get(
            f'/api/vaccination-records/99/'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_records(self):
        response = self.client.get('/api/vaccination-records/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.client.post(
            '/api/vaccination-records/',
            self.record_data,
            format="json",
        )

        response = self.client.get('/api/vaccination-records/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_record(self):
        new_record_data = {
            "pet": self.pet.pk,
            "vaccine": self.vaccine_rabies.pk,
            "veterinarian": self.account.pk,
            "next_dose_recommendation": "2025-06-15"
        }

        response = self.client.put(
            f"/api/vaccination-records/{self.record.pk}/",
            data=new_record_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["vaccine"]["name"], "RABIES")
        self.assertEqual(response.data["next_dose_recommendation"], "2025-06-15")

    def test_update_partial_record(self):
        new_record_data = {
            "vaccine": self.vaccine_rabies.pk,
        }

        response = self.client.patch(
            f"/api/vaccination-records/{self.record.pk}/",
            data=new_record_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["vaccine"]["name"], "RABIES")
        self.assertEqual(response.data["pet"]["name"], "CHOP")

    def test_update_invalid_record(self):
        invalid_record_data = {
            "pet_id": 999,
            "vaccine_id": 999,
        }

        response = self.client.put(
            f"/api/vaccination-records/{self.record.pk}/",
            data=invalid_record_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_partial_record_data = {
            "pet": 999,
        }

        response = self.client.patch(
            f"/api/vaccination-records/{self.record.pk}/",
            data=invalid_partial_record_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

