# infrastructure/models.py
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.validators import MinValueValidator
from utilities.models import User


class AssetType(models.Model):
    """Types of infrastructure assets"""
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    icon = models.CharField(max_length=50, blank=True)  # Font awesome icon class
    color = models.CharField(max_length=7, default='#3b82f6')  # Hex color
    
    class Meta:
        db_table = 'asset_types'
    
    def __str__(self):
        return self.name


class Asset(models.Model):
    """Base model for all infrastructure assets"""
    
    STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('maintenance', 'Under Maintenance'),
        ('faulty', 'Faulty'),
        ('decommissioned', 'Decommissioned'),
    ]
    
    asset_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    asset_type = models.ForeignKey(AssetType, on_delete=models.PROTECT)
    
    # Location
    location = gis_models.PointField()
    address = models.TextField(blank=True)
    
    # Status and condition
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='operational')
    condition_score = models.IntegerField(
        validators=[MinValueValidator(1), MinValueValidator(10)],
        default=10,
        help_text="Asset condition score from 1 (poor) to 10 (excellent)"
    )
    
    # Installation details
    installation_date = models.DateField(null=True, blank=True)
    expected_lifespan = models.IntegerField(help_text="Expected lifespan in years", null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    
    # Maintenance
    last_inspection_date = models.DateTimeField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    
    # Documentation
    manufacturer = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    specifications = models.JSONField(default=dict, blank=True)
    
    # Photos and documents
    primary_image = models.ImageField(upload_to='assets/', null=True, blank=True)
    qr_code = models.ImageField(upload_to='assets/qr/', null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_assets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assets'
        indexes = [
            models.Index(fields=['asset_id']),
            models.Index(fields=['status']),
            models.Index(fields=['asset_type']),
        ]
    
    def __str__(self):
        return f"{self.asset_id} - {self.name}"


class Pipe(models.Model):
    """Water distribution pipes"""
    
    MATERIAL_CHOICES = [
        ('pvc', 'PVC'),
        ('hdpe', 'HDPE'),
        ('steel', 'Steel'),
        ('cast_iron', 'Cast Iron'),
        ('concrete', 'Concrete'),
        ('other', 'Other'),
    ]
    
    pipe_id = models.CharField(max_length=50, unique=True)
    
    # Geometry
    geometry = gis_models.LineStringField()
    length = models.FloatField(validators=[MinValueValidator(0)], help_text="Length in meters")
    
    # Specifications
    diameter = models.FloatField(validators=[MinValueValidator(0)], help_text="Diameter in mm")
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES)
    pressure_rating = models.FloatField(validators=[MinValueValidator(0)], help_text="Pressure rating in bar")
    
    # Network topology
    start_node = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='outgoing_pipes', null=True, blank=True)
    end_node = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='incoming_pipes', null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    installation_date = models.DateField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pipes'
        indexes = [
            models.Index(fields=['pipe_id']),
            models.Index(fields=['material']),
        ]
    
    def __str__(self):
        return f"Pipe {self.pipe_id} - {self.diameter}mm {self.material}"


class Valve(models.Model):
    """Control valves in the network"""
    
    VALVE_TYPE_CHOICES = [
        ('gate', 'Gate Valve'),
        ('butterfly', 'Butterfly Valve'),
        ('ball', 'Ball Valve'),
        ('check', 'Check Valve'),
        ('prv', 'Pressure Reducing Valve'),
        ('air', 'Air Release Valve'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('partially_open', 'Partially Open'),
        ('faulty', 'Faulty'),
    ]
    
    valve_id = models.CharField(max_length=50, unique=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='valve_details')
    
    valve_type = models.CharField(max_length=20, choices=VALVE_TYPE_CHOICES)
    size = models.FloatField(validators=[MinValueValidator(0)], help_text="Size in mm")
    
    # Status
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    last_operation_date = models.DateTimeField(null=True, blank=True)
    operated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Control
    is_remotely_controlled = models.BooleanField(default=False)
    control_id = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'valves'
    
    def __str__(self):
        return f"Valve {self.valve_id} - {self.get_valve_type_display()}"


class Meter(models.Model):
    """Water meters for monitoring consumption"""
    
    METER_TYPE_CHOICES = [
        ('customer', 'Customer Meter'),
        ('bulk', 'Bulk Meter'),
        ('district', 'District Meter'),
        ('production', 'Production Meter'),
    ]
    
    meter_id = models.CharField(max_length=50, unique=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='meter_details')
    
    meter_type = models.CharField(max_length=20, choices=METER_TYPE_CHOICES)
    size = models.FloatField(validators=[MinValueValidator(0)], help_text="Size in mm")
    
    # Customer connection
    customer_account = models.CharField(max_length=50, blank=True)
    
    # Readings
    last_reading = models.FloatField(null=True, blank=True)
    last_reading_date = models.DateTimeField(null=True, blank=True)
    total_consumption = models.FloatField(default=0)
    
    # Smart meter features
    is_smart_meter = models.BooleanField(default=False)
    communication_id = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'meters'
    
    def __str__(self):
        return f"Meter {self.meter_id} - {self.get_meter_type_display()}"


class Zone(models.Model):
    """District Metered Areas (DMAs) or pressure zones"""
    
    ZONE_TYPE_CHOICES = [
        ('dma', 'District Metered Area'),
        ('pressure', 'Pressure Zone'),
        ('service', 'Service Area'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    zone_type = models.CharField(max_length=20, choices=ZONE_TYPE_CHOICES)
    
    # Geometry
    boundary = gis_models.PolygonField()
    
    # Characteristics
    population_served = models.IntegerField(default=0)
    connections = models.IntegerField(default=0)
    
    # Monitoring
    inlet_meters = models.ManyToManyField(Meter, related_name='inlet_zones', blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'zones'
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class AssetDocument(models.Model):
    """Documents attached to assets"""
    
    DOCUMENT_TYPE_CHOICES = [
        ('manual', 'Manual'),
        ('warranty', 'Warranty'),
        ('inspection', 'Inspection Report'),
        ('certification', 'Certification'),
        ('other', 'Other'),
    ]
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='asset_documents/')
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'asset_documents'
    
    def __str__(self):
        return f"{self.title} - {self.asset.asset_id}"


class AssetPhoto(models.Model):
    """Photos of assets"""
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='asset_photos/')
    caption = models.CharField(max_length=200, blank=True)
    
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    taken_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'asset_photos'
        ordering = ['-taken_at']
    
    def __str__(self):
        return f"Photo of {self.asset.asset_id}"