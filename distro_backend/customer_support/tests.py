from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Customer, Ticket
from infrastructure.models import Zone, Meter
from django.contrib.gis.geos import Point

User = get_user_model()

class CustomerSupportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.zone = Zone.objects.create(
            name="Test Zone", code="TZ1", zone_type="dma",
            boundary="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"
        )
        self.meter = Meter.objects.create(
            meter_id="MTR001", meter_type="customer", size=20.0
        )
        self.customer = Customer.objects.create(
            account_number="CUST001", name="Test Customer",
            phone_primary="1234567890", service_address="123 Test St",
            zone=self.zone, meter=self.meter
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.account_number, "CUST001")
        self.assertEqual(str(self.customer), "CUST001 - Test Customer")

    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            title="Test Ticket", description="Test Description",
            ticket_type="complaint", category="leak", priority="high",
            customer=self.customer, reporter_name="Test Reporter",
            reporter_phone="1234567890", source="phone",
            created_by=self.user
        )
        self.assertTrue(ticket.ticket_number.startswith("TKT-"))
        self.assertEqual(str(ticket), f"{ticket.ticket_number} - Test Ticket")