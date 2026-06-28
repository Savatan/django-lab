"""Миграция 0001 — создание таблиц Customer, Product, Cart."""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Телефон')),
                ('registered_at', models.DateTimeField(auto_now_add=True,
                                                       verbose_name='Дата регистрации')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10,
                                              verbose_name='Цена')),
                ('in_stock', models.BooleanField(default=True, verbose_name='В наличии')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('new', 'Новая'), ('paid', 'Оплачена'),
                             ('cancelled', 'Отменена')],
                    default='new', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True,
                                                    verbose_name='Дата создания')),
                ('customer', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='carts', to='store.customer',
                    verbose_name='Покупатель')),
                ('products', models.ManyToManyField(
                    blank=True, related_name='carts', to='store.product',
                    verbose_name='Товары')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
                'ordering': ['-created_at'],
            },
        ),
    ]
