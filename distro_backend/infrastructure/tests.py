from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import AssetType, Asset, Zone
from django.contrib.gis.geos import Point

User = get_user_model()

class InfrastructureTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.asset_type = AssetType.objects.create(name="Pump", code="PMP")
        self.asset = Asset.objects.create(
            asset_id="AST001", name="Test Pump",
            asset_type=self.asset_type, location=Point(0, 0),
            created_by=self.user
        )
        self.zone = Zone.objects.create(
            name="Test Zone", code="TZ1", zone_type="dma",
            boundary="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"
        )

    def test_asset_creation(self):
        self.assertEqual(self.asset.asset_id, "AST001")
        self.assertEqual(str(self.asset), "AST001 - Test Pump")

    def test_zone_creation(self):
        self.assertEqual(self.zone.code, "TZ1")
        self.assertEqual(str(self.zone), "Test Zone (TZ1)")