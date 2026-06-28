"""
seed_data.py — наполнение базы тестовыми данными (Лаба №3).
Запуск:  python3 manage.py shell < seed_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from store.models import Customer, Product, Cart, CartItem

# Очистка
CartItem.objects.all().delete()
Cart.objects.all().delete()
Product.objects.all().delete()
Customer.objects.all().delete()

# ── Покупатели ───────────────────────────────────────────────
customers_data = [
    ('Иван Петров', 'ivan@example.com', '+7 900 111-22-33'),
    ('Мария Сидорова', 'maria@example.com', '+7 900 222-33-44'),
    ('Алексей Смирнов', 'alex@example.com', '+7 900 333-44-55'),
]
customers = [Customer.objects.create(name=n, email=e, phone=p)
             for n, e, p in customers_data]
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
products = [Product.objects.create(name=n, description=d, price=pr, in_stock=s)
            for n, d, pr, s in products_data]
print(f'Создано товаров: {len(products)}')

# ── Корзины с позициями (CartItem с количеством) ─────────────
cart1 = Cart.objects.create(customer=customers[0], status='new', is_active=True)
CartItem.objects.create(cart=cart1, product=products[0], quantity=1)
CartItem.objects.create(cart=cart1, product=products[1], quantity=2)
CartItem.objects.create(cart=cart1, product=products[2], quantity=1)

cart2 = Cart.objects.create(customer=customers[1], status='paid', is_active=True)
CartItem.objects.create(cart=cart2, product=products[3], quantity=1)
CartItem.objects.create(cart=cart2, product=products[5], quantity=3)

# Неактивная (отменённая) корзина
cart3 = Cart.objects.create(customer=customers[2], status='cancelled', is_active=False)
CartItem.objects.create(cart=cart3, product=products[4], quantity=1)

cart4 = Cart.objects.create(customer=customers[0], status='new', is_active=True)
CartItem.objects.create(cart=cart4, product=products[1], quantity=5)

print(f'Создано корзин: {Cart.objects.count()}')
print(f'Создано позиций: {CartItem.objects.count()}')
print('\n✅ База данных заполнена!')
print('Запустите: python3 manage.py runserver')
print('Откройте:  http://127.0.0.1:8000/carts/  и  /admin/')
