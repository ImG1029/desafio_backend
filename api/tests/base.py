from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from api.accounts.models import Account


class BaseAPITestCase(APITestCase):

    def assertUnauthorized(self, response):
        self.assertEqual(response.status_code, 401)

    def assertForbidden(self, response):
        self.assertEqual(response.status_code, 403)

    def assertSuccess(self, response):
        self.assertIn(response.status_code, range(200, 300))


class AuthenticatedAPITestCase(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_superuser(
            username="admin",
            password="admin123",
            first_name="Admin",
            last_name="User"
        )
        cls.admin_account = Account.objects.create(
            user=cls.admin_user,
            license_number=None
        )

        # Create veterinarian
        cls.vet_user = User.objects.create_user(
            username="vet",
            password="vet123",
            first_name="Vet",
            last_name="Doctor"
        )
        cls.vet_account = Account.objects.create(
            user=cls.vet_user,
            license_number="VET-12345"
        )

        # Create regular user
        cls.regular_user = User.objects.create_user(
            username="regular",
            password="regular123",
            first_name="Regular",
            last_name="User"
        )
        cls.regular_account = Account.objects.create(
            user=cls.regular_user,
            license_number=None
        )

    def setUp(self):
        super().setUp()
        self.authenticate_as_vet()

    def authenticate_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

    def authenticate_as_vet(self):
        self.client.force_authenticate(user=self.vet_user)

    def authenticate_as_regular(self):
        self.client.force_authenticate(user=self.regular_user)

    def unauthenticate(self):
        from rest_framework.test import APIClient
        self.client = APIClient()  # Create a fresh unauthenticated client
