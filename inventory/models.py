from django.db import models

# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.sku})" if self.sku else self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Batch(models.Model):
    medicine_name = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=50)
    expiry_date = models.DateField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length=20)
    purchase_price = models.FloatField()
    supplier_name = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('medicine_name', 'batch_no')
        ordering = ['expiry_date']

    def __str__(self):
        return f"{self.medicine_name.name} - {self.batch_no}"