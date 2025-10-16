from django.contrib import admin

# Register your models here.
from .models import Medicine, Supplier, Batch
admin.site.register(Medicine)
admin.site.register(Supplier)
admin.site.register(Batch)