from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Issue
from infrastructure.models import Asset, AssetType
from django.contrib.gis.geos import Point

User = get_user_model()

class MaintenanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.asset_type = AssetType.objects.create(name="Pump", code="PMP")
        self.asset = Asset.objects.create(
            asset_id="AST001", name="Test Pump",
            asset_type=self.asset_type, location=Point(0, 0),
            created_by=self.user
        )
        self.issue = Issue.objects.create(
            title="Test Issue", description="Test Description",
            issue_type="leak", priority="high", status="reported",
            location=Point(0, 0), reported_by=self.user
        )

    def test_issue_creation(self):
        self.assertTrue(self.issue.issue_id.startswith("LEA-"))
        self.assertEqual(str(self.issue), f"{self.issue.issue_id} - Test Issue")