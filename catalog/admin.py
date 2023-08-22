from django.contrib import admin

from catalog.models import Product, Category, Blog, Version


@admin.register(Product)
class ProductAdmine(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ['category']
    search_fields = ['name', 'description']

@admin.register(Version)
class VersionAdmine(admin.ModelAdmin):
    list_display = ('id', 'product', 'number', 'version_name', 'status',)
    list_filter = ['product']
    search_fields = ['product', 'version_name', 'status']

@admin.register(Category)
class CategoryAdmine(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Blog)
class BlogAdmine(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'preview', 'created_date', 'published_status', 'views_count')
    list_filter = ['published_status']
    search_fields = ['title', 'content']

