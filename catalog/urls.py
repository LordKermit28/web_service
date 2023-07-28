
from django.urls import path
from catalog.views import index, information_page

urlpatterns = [
    path('', index),
    path('', information_page)
]
