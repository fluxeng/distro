from django.test import TestCase
from .models import Utility

class TenantsTests(TestCase):
    def setUp(self):
        self.utility = Utility.objects.create(
            name="Test Utility",
            schema_name="test_utility",
            contact_email="test@utility.com",
            contact_phone="1234567890"
        )

    def test_utility_creation(self):
        self.assertEqual(self.utility.name, "Test Utility")
        self.assertEqual(str(self.utility), "Test Utility")