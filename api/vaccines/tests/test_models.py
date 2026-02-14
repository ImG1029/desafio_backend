from rest_framework.test import APITestCase

from api.vaccines.models import Vaccine

class VaccineModelTest(APITestCase):
    def setUp(self):
        self.vaccine = Vaccine.objects.create(
            name="VACCINE NAME",
            type="VACCINE TYPE",
            manufacturer="VACCINE MANUFACTURER",
        )

    def test_vaccines(self):
        self.assertEqual(self.vaccine.name, "VACCINE NAME")
        self.assertEqual(self.vaccine.type, "VACCINE TYPE")
        self.assertEqual(self.vaccine.manufacturer, "VACCINE MANUFACTURER")