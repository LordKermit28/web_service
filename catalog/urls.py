from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.services import get_categories
from catalog.views import index, contacts, ProductListView, ProductDetailView, BlogListView, BlogDetailView, \
    BlogCreateView, BlogUpdateView, BlogDeleteView, switch_status, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, switch_status_product, CategoryListView

urlpatterns = [
    path('', index),
    path('', contacts),
    path('list_product', ProductListView.as_view(), name='list_product'),
    path('view_product/<int:pk>/', ProductDetailView.as_view(),  name='view_product'),
    path('create_product', ProductCreateView.as_view(), name='create_product'),
    path('delete_product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('edit_product/<int:pk>/', ProductUpdateView.as_view(),  name='edit_product'),
    path('list_blog', cache_page(60)(BlogListView.as_view()), name='list_blog'),
    path('view_blog/<str:slug>//', BlogDetailView.as_view(),  name='view_blog'),
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(),  name='edit_blog'),
    path('delete_blog/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog'),
    path('switch_status/<int:pk>/', switch_status, name='switch_status'),
    path('switch_status_product/<int:pk>/', switch_status_product, name='switch_status_product'),
    path('categories/', CategoryListView.as_view(), name='categories'),
]
