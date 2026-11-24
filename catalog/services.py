from django.core.cache import cache
from django.db.models import QuerySet

from .models import Product


def get_products_by_category(category_id: int) -> QuerySet[Product]:
    """Возвращает список продуктов указанной категории с кешированием в Redis."""
    cache_key = f"category_{category_id}"
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(category_id=category_id)
        cache.set(cache_key, products, 60 * 15)  # TTL 15 минут

    return products  # type: ignore[no-any-return]


def get_all_products() -> QuerySet[Product]:
    """Низкоуровневое кеширование общего списка продуктов."""
    cache_key = "products_list"
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.all()
        cache.set(cache_key, products, 60 * 15)  # TTL 15 минут

    return products  # type: ignore[no-any-return]
