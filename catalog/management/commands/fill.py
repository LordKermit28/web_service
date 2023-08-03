from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Создание категорий
        category_list = [
            {'name': 'Electronics', 'describing': ""},
            {'name': 'Clothing', 'describing': ""},
            {'name': 'Books', 'describing': ""},
            # Добавьте другие категории по вашему желанию
        ]

        categories = []
        for category in category_list:
            categories.append(Category(**category))

        Category.objects.bulk_create(categories)

        product_list = [
            {'name': 'Phone', 'price': 1000, 'category': Category.objects.get(name='Electronics')},
            {'name': 'T-Shirt', 'price': 20, 'category': Category.objects.get(name='Clothing')},
            {'name': 'Book', 'price': 15, 'category': Category.objects.get(name='Books')},
        ]
        products = []
        for product in product_list:
            products.append(Product(**product))
        Product.objects.bulk_create(products)