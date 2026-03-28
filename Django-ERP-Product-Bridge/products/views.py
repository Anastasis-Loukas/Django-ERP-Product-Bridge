from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm
from .services import sync_products
#from django.http import HttpResponse

# Create your views here.

@login_required(login_url='login')
def products_home(request):
    if request.method == "POST":
        sync_products()
        return redirect('products:list')
    return render(request, "products/products_home.html")
    
@login_required(login_url='login')   
def products_list(request):
        products = Product.objects.all()
        return render(request, "products/products_list.html", {
        "products": products})
    #return HttpResponse("PRODUCTS PAGE WORKS")

# ==============================
# CREATE
# ==============================
@login_required(login_url='login')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:list')
    else:
        form = ProductForm()

    return render(request, 'products/form.html', {
        'form': form,
        'title': 'Create Product'
    })


# ==============================
# EDIT
# ==============================
@login_required(login_url='login')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/form.html', {
        'form': form,
        'title': 'Edit Product'
    })


# ==============================
# DELETE
# ==============================
@login_required(login_url='login')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('products:list')

    return render(request, 'products/confirm_delete.html', {
        'product': product
    })