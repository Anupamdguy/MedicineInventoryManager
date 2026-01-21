# assistant/models.py
"""
Example models structure for reference
Adjust based on your actual inventory/models.py
"""

from django.db import models
from django.utils import timezone


class Supplier(models.Model):
    """Medicine Supplier"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Medicine(models.Model):
    """Medicine/Drug Model"""
    CATEGORY_CHOICES = [
        ('ANTIBIOTIC', 'Antibiotic'),
        ('PAINKILLER', 'Painkiller'),
        ('ANTIVIRAL', 'Antiviral'),
        ('ANTIHISTAMINE', 'Antihistamine'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    manufacturer = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='OTHER')
    description = models.TextField(blank=True)
    
    # Stock information
    current_stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Dates
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.generic_name})"
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.reorder_level
    
    @property
    def is_expired(self):
        return self.expiry_date and self.expiry_date < timezone.now().date()
    
    @property
    def days_until_expiry(self):
        if self.expiry_date:
            delta = self.expiry_date - timezone.now().date()
            return delta.days
        return None
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Medicines'


class Batch(models.Model):
    """Batch/Lot tracking for medicines"""
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.medicine.name} - Batch {self.batch_number}"
    
    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()
    
    class Meta:
        ordering = ['expiry_date']
        verbose_name_plural = 'Batches'


class Transaction(models.Model):
    """Stock transaction tracking"""
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('RETURN', 'Return'),
        ('ADJUSTMENT', 'Adjustment'),
    ]
    
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    transaction_date = models.DateTimeField(default=timezone.now)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    user = models.CharField(max_length=100, blank=True)  # Or ForeignKey to User model
    
    def __str__(self):
        return f"{self.transaction_type} - {self.medicine.name} ({self.quantity})"
    
    class Meta:
        ordering = ['-transaction_date']


class Alert(models.Model):
    """System alerts for low stock, expiry, etc."""
    ALERT_TYPES = [
        ('LOW_STOCK', 'Low Stock'),
        ('OUT_OF_STOCK', 'Out of Stock'),
        ('EXPIRING_SOON', 'Expiring Soon'),
        ('EXPIRED', 'Expired'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('RESOLVED', 'Resolved'),
        ('IGNORED', 'Ignored'),
    ]
    
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.alert_type} - {self.medicine.name}"
    
    class Meta:
        ordering = ['-created_at']
