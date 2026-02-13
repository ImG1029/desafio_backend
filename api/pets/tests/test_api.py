from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase
from rest_framework import status
from api.pets.models import Pet

class TestPetAPI(APITestCase):
    def setUp(self):
        self.pet_data = {
            "name": "TEST DOG",
            "species": "TEST SPECIES",
            "breed": "TEST BREED",
            "birth_date": "2000-12-31"
        }

        self.pet = Pet.objects.create(
            name="TODDY",
            species="DOG",
            breed="LHASA APSO",
            birth_date="2019-06-27"
        )

    def test_create_pet(self):
        response = self.client.post(
            "/api/pets/",
            self.pet_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "TEST DOG")

    def test_list_pets(self):
        response = self.client.get("/api/pets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_pet(self):
        response = self.client.get(
            f"/api/pets/{self.pet.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "TODDY")

    def test_update_pet(self):
        new_pet_data = {
            "name": "TEST DOG 2",
            "species": "TEST SPECIES 2",
            "breed": "TEST BREED 2",
            "birth_date": "2020-10-15"
        }

        response = self.client.put(
            f"/api/pets/{self.pet.id}/",
            data=new_pet_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "TEST DOG 2")

    def test_delete_pet(self):
        response = self.client.delete(
            f"/api/pets/{self.pet.id}/"
        )

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)