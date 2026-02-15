from django.db import IntegrityError
from django.test import TestCase

from api.owners.models import Owner
from api.pets.models import Pet

class PetModelTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            name="TEST NAME",
            cpf=11111111111,
            email="test@email.com",
            phone_number=34987654321,
            address="RUA DO TESTE",
            address_2=123
        )

        self.pet = Pet.objects.create(
            name="TEST DOG",
            species="TEST SPECIES",
            breed="TEST BREED",
            birth_date="2000-12-31",
            owner_id=1
        )

    def test_pets_creation(self):
        self.assertEqual(self.pet.name, "TEST DOG")
        self.assertEqual(self.pet.species, "TEST SPECIES")
        self.assertEqual(self.pet.breed, "TEST BREED")
        self.assertEqual(self.pet.birth_date, "2000-12-31")
