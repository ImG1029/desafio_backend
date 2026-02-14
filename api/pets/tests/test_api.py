from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.test import APITestCase
from rest_framework import status

from api.owners.models import Owner
from api.pets.models import Pet

class TestPetAPI(APITestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            name="TEST NAME",
            cpf=11111111111,
            email="test@email.com",
            phone_number=34987654321,
            address="RUA DO TESTE",
            address_2=123
        )

        self.pet_data = {
            "name": "TEST DOG",
            "species": "TEST SPECIES",
            "breed": "TEST BREED",
            "birth_date": "2000-12-31",
            "owner": 1
        }

        self.invalid_pet_data = {
            "name": "INVALID DOG",
            "species": "TEST SPECIES",
            "breed": "TEST BREED",
            "birth_date": 2000-12-31,
            "owner": 1
        }

        self.pet = Pet.objects.create(
            name="TODDY",
            species="DOG",
            breed="LHASA APSO",
            birth_date="2019-06-27",
            owner_id=1
        )

        self.pet2 = Pet.objects.create(
            name="TODDY 2",
            species="DOG",
            breed="LHASA APSO",
            birth_date="2019-06-27",
            owner_id=1
        )

        self.pet3 = Pet.objects.create(
            name="TODDY 3",
            species="DOG",
            breed="LHASA APSO",
            birth_date="2019-06-27",
            owner_id=1
        )

    def test_create_pet(self):
        response = self.client.post(
            "/api/pets/",
            self.pet_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "TEST DOG")

    def test_create_invalid_pet(self):
        response = self.client.post(
            "/api/pets/",
            self.invalid_pet_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_pets(self):
        response = self.client.get("/api/pets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_pet(self):
        response = self.client.get(
            f"/api/pets/{self.pet.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "TODDY")

    def test_retrieve_invalid_pet(self):
        response = self.client.get("/api/pets/99/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_pet(self):
        new_pet_data = {
            "name": "PUTTED",
            "species": "TEST SPECIES 2",
            "breed": "TEST BREED 2",
            "birth_date": "2020-10-15",
            "owner": 1
        }

        response = self.client.put(
            f"/api/pets/{self.pet.id}/",
            data=new_pet_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "PUTTED")

    def test_patch_pet(self):
        new_pet_data = {
            "name": "PATCHED",
            "species": "TEST SPECIES",
            "breed": "TEST BREED",
            "birth_date": "2000-12-31",
            "owner": 1
        }

        response = self.client.patch(
            f"/api/pets/{self.pet.id}/",
            data=new_pet_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "PATCHED")

    def test_put_invalid_pet(self):
        new_pet_data = {
            "name": "PUTTED",
            "species": "TEST SPECIES 2",
            "breed": "TEST BREED 2",
            "birth_date": 2020-10-15,
            "owner": 1
        }

        response = self.client.put(
            f"/api/pets/{self.pet.id}/",
            data=new_pet_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_pet(self):
        response = self.client.delete(
            f"/api/pets/{self.pet.id}/"
        )

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_delete_invalid_pet(self):
        self.client.delete(
            f"/api/pets/{self.pet.id}/"
        )
        response = self.client.delete(
            f"/api/pets/{self.pet.id}/"
        )

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)