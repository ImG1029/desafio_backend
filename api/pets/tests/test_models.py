from rest_framework.test import APITestCase

from api.pets.models import Pet

class PetModelTest(APITestCase):
    def setUp(self):
        self.pet = Pet.objects.create(
            name="TEST DOG",
            species="TEST SPECIES",
            breed="TEST BREED",
            birth_date="2000-12-31"
        )

    def test_pets_creation(self):
        self.assertEqual(self.pet.name, "TEST DOG")
        self.assertEqual(self.pet.species, "TEST SPECIES")
        self.assertEqual(self.pet.breed, "TEST BREED")
        self.assertEqual(self.pet.birth_date, "2000-12-31")
