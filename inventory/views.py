from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from .models import Medicine, Batch, Supplier
from .forms import MedicineForm, BatchForm, SupplierForm
from django.db.models import Sum

# ============= INDEX PAGE =============
def index(request):
    medicines = Medicine.objects.all()
    
    # Get total inventory stats
    total_medicines = medicines.count()
    total_batches = Batch.objects.count()
    total_suppliers = Supplier.objects.count()
    
    # Remove the error check to allow viewing empty state
    # if total_medicines == 0 or total_batches == 0 or total_suppliers == 0:
    #     ... removed
    
    # Get medicines with their total quantities
    medicine_data = []
    for medicine in medicines:
        batches = Batch.objects.filter(medicine_name=medicine)
        total_quantity = batches.aggregate(Sum('quantity'))['quantity__sum'] or 0
        medicine_data.append({
            'medicine': medicine,
            'total_quantity': total_quantity,
            'batches': batches
        })
    
    context = {
        'medicine_data': medicine_data,
        'total_medicines': total_medicines,
        'total_batches': total_batches,
        'total_suppliers': total_suppliers,
    }
    return render(request, 'index.html', context)

# ============= MEDICINE VIEWS =============
def medicine_list(request):
    medicines = Medicine.objects.all().order_by('name')
    context = {
        'medicines': medicines,
        'total': medicines.count(),
    }
    return render(request, 'medicine_list.html', context)

def medicine_add(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save()
            messages.success(request, f'Medicine "{medicine.name}" added successfully!')
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    
    return render(request, 'medicine_form.html', {'form': form, 'title': 'Add Medicine'})

def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, f'Medicine "{medicine.name}" updated successfully!')
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    
    return render(request, 'medicine_form.html', {'form': form, 'title': 'Edit Medicine'})

def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        name = medicine.name
        medicine.delete()
        messages.success(request, f'Medicine "{name}" deleted successfully!')
        return redirect('medicine_list')
    
    return render(request, 'medicine_confirm_delete.html', {'medicine': medicine})

# ============= SUPPLIER VIEWS =============
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')
    context = {
        'suppliers': suppliers,
        'total': suppliers.count(),
    }
    return render(request, 'supplier_list.html', context)

def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier "{supplier.name}" added successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, 'supplier_form.html', {'form': form, 'title': 'Add Supplier'})

def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, f'Supplier "{supplier.name}" updated successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'supplier_form.html', {'form': form, 'title': 'Edit Supplier'})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        name = supplier.name
        supplier.delete()
        messages.success(request, f'Supplier "{name}" deleted successfully!')
        return redirect('supplier_list')
    
    return render(request, 'supplier_confirm_delete.html', {'supplier': supplier})

# ============= BATCH VIEWS =============
def batch_list(request):
    batches = Batch.objects.all().select_related('medicine_name', 'supplier_name').order_by('expiry_date')
    context = {
        'batches': batches,
        'total': batches.count(),
    }
    return render(request, 'batch_list.html', context)

def batch_add(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save()
            messages.success(request, f'Batch "{batch.batch_no}" added successfully!')
            return redirect('batch_list')
    else:
        form = BatchForm()
    
    return render(request, 'batch_form.html', {'form': form, 'title': 'Add Batch'})

def batch_edit(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, f'Batch "{batch.batch_no}" updated successfully!')
            return redirect('batch_list')
    else:
        form = BatchForm(instance=batch)
    
    return render(request, 'batch_form.html', {'form': form, 'title': 'Edit Batch'})

def batch_delete(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        batch_no = batch.batch_no
        batch.delete()
        messages.success(request, f'Batch "{batch_no}" deleted successfully!')
        return redirect('batch_list')
    
    return render(request, 'batch_confirm_delete.html', {'batch': batch})