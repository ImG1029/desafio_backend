from rest_framework import status
from rest_framework.test import APITestCase

from api.vaccines.models import Vaccine

class TestVaccineAPI(APITestCase):
    def setUp(self):
        self.vaccine_data = {
            "name": "NEW VACCINE NAME",
            "type": "VACCINE TYPE",
            "manufacturer": "VACCINE MANUFACTURER",
            "recommended_interval_days": 365,
        }

        self.invalid_vaccine_data = {
            "nome": "INVALID VACCINE NAME",
            "top": "VACCINE TYPE",
            "manufacture": "VACCINE MANUFACTURER",
            "recommended_interval_days": 365,
        }

        self.vaccine = Vaccine.objects.create(
            name="VACCINE NAME",
            type="VACCINE TYPE",
            manufacturer="VACCINE MANUFACTURER"
        )

    def test_create_vaccine(self):
        response = self.client.post(
            "/api/vaccines/",
            self.vaccine_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "NEW VACCINE NAME")

    def test_create_invalid_vaccine(self):
        response = self.client.post(
            "/api/vaccines/",
            self.invalid_vaccine_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_vaccine(self):
        response = self.client.get(
            f"/api/vaccines/{self.vaccine.pk}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "VACCINE NAME")

    def test_retrieve_invalid_vaccine(self):
        response = self.client.get(
            f"/api/vaccines/99/",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_vaccines(self):
        response = self.client.get("/api/vaccines/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.client.post(
            "/api/vaccines/",
            self.vaccine_data,
            format="json"
        )

        response = self.client.get("/api/vaccines/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_vaccine(self):
        new_vaccine_data = {
            "name": "UPDATED VACCINE NAME",
            "type": "UPDATED VACCINE TYPE",
            "manufacturer": "UPDATED VACCINE MANUFACTURER",
            "recommended_interval_days": 5,
        }

        response = self.client.put(
            f"/api/vaccines/{self.vaccine.pk}/",
            data=new_vaccine_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "UPDATED VACCINE NAME")
        self.assertEqual(response.data["type"], "UPDATED VACCINE TYPE")
        self.assertEqual(response.data["manufacturer"], "UPDATED VACCINE MANUFACTURER")

    def test_update_vaccine_partial(self):
        new_vaccine_data = {
            "name": "UPDATED VACCINE NAME",
        }

        response = self.client.patch(
            f"/api/vaccines/{self.vaccine.pk}/",
            data=new_vaccine_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "UPDATED VACCINE NAME")
        self.assertEqual(response.data["type"], "VACCINE TYPE")
        self.assertEqual(response.data["manufacturer"], "VACCINE MANUFACTURER")

    def test_update_invalid_vaccine(self):
        new_invalid_vaccine_data = {
            "name": "UPDATED VACCINE NAME",
            "type": "UPDATED VACCINE TYPE",
            "manufacture": "UPDATED VACCINE MANUFACTURER",
        }

        response = self.client.put(
            f"/api/vaccines/{self.vaccine.pk}/",
            data=new_invalid_vaccine_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_vaccine(self):
        response = self.client.delete(
            f"/api/vaccines/{self.vaccine.pk}/",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_vaccine(self):
        self.client.delete(
            f"/api/vaccines/{self.vaccine.pk}/",
        )
        response = self.client.delete(
            f"/api/vaccines/{self.vaccine.pk}/",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
