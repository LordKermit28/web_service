from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def index(request):
    return render(request, 'catalog/index.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(name, phone, message)
    return render(request, 'catalog/contacts.html')


def products(request):
    products_list = Product.objects.all()
    context = {
        'objects_list': products_list
    }
    return render(request, 'catalog/products.html', context)

from django.shortcuts import get_object_or_404

def product(request, id):
    product = get_object_or_404(Product, id=id)

    context = {
        'product': product
    }
    return render(request, 'catalog/product.html', context)