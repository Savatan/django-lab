from django.contrib import admin
from .models import Customer, Product, Cart


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'registered_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['registered_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'in_stock', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['in_stock', 'created_at']
    list_editable = ['price', 'in_stock']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # Основная информация в списке корзин + количество товаров
    list_display = ['id', 'customer', 'status', 'total_items', 'total_price', 'created_at']
    # Фильтрация по статусу, дате и покупателю
    list_filter = ['status', 'created_at', 'customer']
    # Поиск по имени и email покупателя
    search_fields = ['customer__name', 'customer__email']
    # Удобный виджет выбора товаров
    filter_horizontal = ['products']
    # Навигация по дате
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
