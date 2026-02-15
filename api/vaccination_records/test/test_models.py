from django.contrib.auth.models import User
from django.test import TestCase

from api.vaccination_records.models import VaccinationRecord
from api.owners.models import Owner
from api.accounts.models import Account
from api.pets.models import Pet
from api.vaccines.models import Vaccine

class VaccinationRecordTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            name="FRANKLIN",
            cpf=11111111111,
            email="test@email.com",
            phone_number=34987654321,
            address="RUA DO TESTE",
            address_2=123
        )

        self.pet = Pet.objects.create(
            name="CHOP",
            species="DOG",
            breed="ROTTWEILER",
            birth_date="2000-12-31",
            owner_id=1
        )

        self.vaccine = Vaccine.objects.create(
            name="VACCINE NAME",
            type="VACCINE TYPE",
            manufacturer="VACCINE MANUFACTURER",
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
            veterinarian=self.account
        )

    def test_vaccination_record_creation(self):
        self.assertEqual(self.record.pet.name, "CHOP")
        self.assertEqual(self.record.vaccine.name, "VACCINE NAME")
        self.assertEqual(self.record.veterinarian.user.username, "VET USERNAME")
        self.assertIsNotNone(self.record.vaccinated_at)