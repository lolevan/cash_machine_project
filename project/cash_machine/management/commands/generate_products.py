from django.core.management.base import BaseCommand
from ...models import Item
import random


class Command(BaseCommand):
    help = 'Генератор 5 рандомных продуктов'

    def handle(self, *args, **kwargs):
        products = [
            {'title': 'Товар 1', 'price': random.uniform(100.0, 1000.0)},
            {'title': 'Товар 2', 'price': random.uniform(100.0, 1000.0)},
            {'title': 'Товар 3', 'price': random.uniform(100.0, 1000.0)},
            {'title': 'Товар 4', 'price': random.uniform(100.0, 1000.0)},
            {'title': 'Товар 5', 'price': random.uniform(100.0, 1000.0)},
        ]

        for product in products:
            item = Item.objects.create(title=product['title'], price=round(product['price'], 2))
            self.stdout.write(self.style.SUCCESS(f'Создан продукт: {item.title} с ценой {item.price}'))
