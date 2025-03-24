from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


class ProductService:

    @staticmethod
    def get_products_by_category(category_id):
        """Возвращаем список продуктов для заданной категории"""
        products = Product.objects.filter(category_id=category_id)
        return products

    @staticmethod
    def get_products_list():
        """При отключенном кешировании получаем данные из БД, иначе проверяем кеш,
         и возвращаем данные из кеша, если он не пуст."""
        if not CACHE_ENABLED:
            return Product.objects.all()

        key = 'products_list'
        products = cache.get(key)
        if products is None:
            products = Product.objects.all()
            cache.set(key, products)
            return products
        return products
