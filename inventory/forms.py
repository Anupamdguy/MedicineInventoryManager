from django import forms
from .models import Medicine, Batch, Supplier

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'sku', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Medicine name'}),
            'sku': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'SKU (e.g., MED001)'}),
            'category': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Category'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Description'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Supplier name'}),
            'contact': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Contact (email/phone)'}),
        }

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['medicine_name', 'batch_no', 'expiry_date', 'quantity', 'unit', 'purchase_price', 'supplier_name']
        widgets = {
            'medicine_name': forms.Select(attrs={'class': 'form-input'}),
            'batch_no': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Batch number'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Quantity'}),
            'unit': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Unit (e.g., tablets, vials)'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Price'}),
            'supplier_name': forms.Select(attrs={'class': 'form-input'}),
        }