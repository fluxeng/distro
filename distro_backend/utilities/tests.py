from django.test import TestCase
from .models import User, Department

class UtilitiesTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Maintenance")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            department=self.department
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(str(self.user), "testuser")

    def test_department_creation(self):
        self.assertEqual(self.department.name, "Maintenance")
        self.assertEqual(str(self.department), "Maintenance")