import csv
from django.core.management.base import BaseCommand
from inventory.models import Medicine, Supplier, Batch
from datetime import datetime

class Command(BaseCommand):
    help = 'Load sample data from CSV files'

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Batch.objects.all().delete()
        Medicine.objects.all().delete()
        Supplier.objects.all().delete()
        
        # Load Medicines
        self.stdout.write('Loading medicines...')
        with open('sample_data/medicines.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            medicines_created = 0
            for row in reader:
                Medicine.objects.create(
                    name=row['name'],
                    sku=row['sku'],
                    category=row['category'],
                    description=row['description']
                )
                medicines_created += 1
        self.stdout.write(self.style.SUCCESS(f'✓ Created {medicines_created} medicines'))
        
        # Load Suppliers
        self.stdout.write('Loading suppliers...')
        with open('sample_data/suppliers.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            suppliers_created = 0
            for row in reader:
                Supplier.objects.create(
                    name=row['name'],
                    contact=row['contact']
                )
                suppliers_created += 1
        self.stdout.write(self.style.SUCCESS(f'✓ Created {suppliers_created} suppliers'))
        
        # Load Batches
        self.stdout.write('Loading batches...')
        with open('sample_data/batches.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            batches_created = 0
            for row in reader:
                medicine = Medicine.objects.get(name=row['medicine_name'])
                supplier = Supplier.objects.get(name=row['supplier_name'])
                
                # Parse date from YYYY-MM-DD format
                expiry_date = datetime.strptime(row['expiry_date'], '%Y-%m-%d').date()
                
                Batch.objects.create(
                    medicine_name=medicine,
                    batch_no=row['batch_no'],
                    expiry_date=expiry_date,
                    quantity=int(row['quantity']),
                    unit=row['unit'],
                    purchase_price=float(row['purchase_price']),
                    supplier_name=supplier
                )
                batches_created += 1
        self.stdout.write(self.style.SUCCESS(f'✓ Created {batches_created} batches'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 All sample data loaded successfully!'))