from django.shortcuts import render

from catalog.models import Product


def index(request):
    return render(request, 'main/index.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(name, phone, message)
    return render(request, 'main/contacts.html')


def products(request):
    products_list = Product.objects.all()
    content = {
        'objects_lict': products_list
    }
    return render(request, 'main/products.html', content)

def product(request):
    return render(request, 'main/product.html')