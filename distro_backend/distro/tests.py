from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from .models import AssetType, Asset, Issue

UserProfile = get_user_model()

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = UserProfile.objects.create_user(
            username='admin', password='admin123', role='ADMIN'
        )
        self.technician = UserProfile.objects.create_user(
            username='technician', password='tech123', role='FIELD_TECHNICIAN'
        )
        self.asset_type = AssetType.objects.create(name='Pipe')
        self.asset = Asset.objects.create(
            name='TURK-PIPE-001',
            asset_type=self.asset_type,
            geometry='LINESTRING(35.0 0.0, 35.1 0.1)'
        )

    def test_create_asset_type(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/asset-types/', {'name': 'Valve', 'description': 'Water valve'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AssetType.objects.count(), 2)

    def test_create_asset_type_unauthorized(self):
        self.client.force_authenticate(user=self.technician)
        response = self.client.post('/api/asset-types/', {'name': 'Valve', 'description': 'Water valve'})
        self.assertEqual(response.status_code, 403)

    def test_filter_assets_by_bbox(self):
        self.client.force_authenticate(user=self.admin)
        bbox = [34.9, -0.1, 35.2, 0.2]
        response = self.client.post('/api/assets/filter_by_bbox/', {'bbox': bbox})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'TURK-PIPE-001')

    def test_create_issue(self):
        self.client.force_authenticate(user=self.technician)
        data = {
            'title': 'Leaking Pipe',
            'description': 'Pipe leaking in Turkana',
            'location': 'POINT(35.0 0.0)',
            'reported_by_id': self.technician.id,
            'priority': 'HIGH',
            'status': 'REPORTED'
        }
        response = self.client.post('/api/issues/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Issue.objects.count(), 1)