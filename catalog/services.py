from django.core.cache import cache
from django.views.decorators.cache import cache_page

from catalog.models import Category

def get_categories():
    categories = cache.get('categories')

    if not categories:
        categories = list(Category.objects.all())
        cache.set('categories', categories)

    return categories