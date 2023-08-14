
from django.urls import path
from catalog.views import index, contacts, products, product

urlpatterns = [
    path('', index),
    path('contacts/', contacts),
    path('products/', products),
    path('products/<int:id>', product, name='product'),
]
