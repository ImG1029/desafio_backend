from rest_framework.test import APITestCase

from api.owners.models import Owner


class OwnerModelTest(APITestCase):

    def setUp(self):
        self.owner = Owner.objects.create(
            name="TEST NAME",
            cpf=11111111111,
            email="test@email.com",
            phone_number=34987654321,
            address="RUA DO TESTE",
            address_2=123
        )

    def test_owner_creation(self):
        self.assertEqual(self.owner.name, "TEST NAME")
        self.assertEqual(self.owner.cpf, 11111111111)
        self.assertEqual(self.owner.email, "test@email.com")
        self.assertEqual(self.owner.phone_number, 34987654321)
        self.assertEqual(self.owner.address, "RUA DO TESTE")
        self.assertEqual(self.owner.address_2, 123)
