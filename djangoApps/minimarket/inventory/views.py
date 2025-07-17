from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Transaction
from .forms import ProductForm, TransactionForm

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'inventory/home.html', {'products': products})

def product_detail(request, pk):
    product =get_object_or_404(Product, pk=pk)
    transactions = Transaction.objects.filter(product=product)
    return render(request, 'inventory/product_detail.html', {'product': product, 'transactions': transactions})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
        return render(request, 'inventory/add_product.html', {'form': form})
    
def add_transaction(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.save()
            return redirect('product_detail', pk=product.id)
    else:
        form = TransactionForm()
    return render(request, 'inventory/add_transaction.html', {'form': form, 'product': product})

