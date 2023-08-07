from django.contrib import admin

from catalog.models import Product, Category

# Register your models here.
# admin.site.register(Product)
# admin.site.register(Category)


@admin.register(Product)
class ProductAdmine(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category_id')
    list_filter = ['category_id']
    search_fields = ['name', 'description']

@admin.register(Category)
class CategoryAdmine(admin.ModelAdmin):
    list_display = ('id', 'name')

