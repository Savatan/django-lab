"""
seed_data.py — наполнение базы тестовыми данными.
Запуск:  python3 manage.py shell < seed_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from store.models import Customer, Product, Cart

# Очистка
Cart.objects.all().delete()
Product.objects.all().delete()
Customer.objects.all().delete()

# ── Покупатели ───────────────────────────────────────────────
customers_data = [
    ('Иван Петров', 'ivan@example.com', '+7 900 111-22-33'),
    ('Мария Сидорова', 'maria@example.com', '+7 900 222-33-44'),
    ('Алексей Смирнов', 'alex@example.com', '+7 900 333-44-55'),
]
customers = []
for name, email, phone in customers_data:
    customers.append(Customer.objects.create(name=name, email=email, phone=phone))
print(f'Создано покупателей: {len(customers)}')

# ── Товары ───────────────────────────────────────────────────
products_data = [
    ('Ноутбук ASUS', 'Игровой ноутбук 15.6"', 65000, True),
    ('Мышь Logitech', 'Беспроводная мышь', 2500, True),
    ('Клавиатура механическая', 'RGB-подсветка', 5500, True),
    ('Монитор 27"', '4K IPS дисплей', 28000, True),
    ('Наушники Sony', 'С шумоподавлением', 18000, False),
    ('Веб-камера', 'Full HD 1080p', 4200, True),
]
products = []
for name, desc, price, stock in products_data:
    products.append(Product.objects.create(
        name=name, description=desc, price=price, in_stock=stock))
print(f'Создано товаров: {len(products)}')

# ── Корзины ──────────────────────────────────────────────────
cart1 = Cart.objects.create(customer=customers[0], status='new')
cart1.products.set([products[0], products[1], products[2]])

cart2 = Cart.objects.create(customer=customers[1], status='paid')
cart2.products.set([products[3], products[5]])

cart3 = Cart.objects.create(customer=customers[2], status='cancelled')
cart3.products.set([products[4]])

cart4 = Cart.objects.create(customer=customers[0], status='new')
cart4.products.set([products[1]])

print(f'Создано корзин: {Cart.objects.count()}')
print('\n✅ База данных заполнена!')
print('Запустите: python3 manage.py runserver')
print('Откройте:  http://127.0.0.1:8000/carts/')
