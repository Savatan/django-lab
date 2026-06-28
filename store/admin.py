from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Product, Cart, CartItem


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


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    autocomplete_fields = ['product']
    readonly_fields = ['subtotal_display']

    def subtotal_display(self, obj):
        if obj and obj.pk:
            return f'{obj.subtotal()} руб.'
        return '—'
    subtotal_display.short_description = 'Подытог'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'cart_label', 'customer', 'colored_status', 'is_active',
        'total_quantity', 'total_price_display', 'created_at',
    ]
    list_filter = ['status', 'is_active', 'created_at', 'customer']
    search_fields = ['customer__name', 'customer__email']
    date_hierarchy = 'created_at'      
    inlines = [CartItemInline]          
    readonly_fields = ['created_at', 'summary_block']
    fieldsets = [
        (None, {
            'fields': ['customer', 'status', 'is_active', 'created_at'],
        }),
        ('Итоги корзины', {
            'fields': ['summary_block'],
        }),
    ]

    def cart_label(self, obj):
        if not obj.is_active:
            return format_html(
                '<span style="color:#999;text-decoration:line-through;">'
                'Корзина #{} (неактивна)</span>', obj.pk)
        return format_html('<strong>Корзина #{}</strong>', obj.pk)
    cart_label.short_description = 'Корзина'

    def colored_status(self, obj):
        colors = {'new': '#1877f2', 'paid': '#1a7a35', 'cancelled': '#d32f2f'}
        return format_html(
            '<span style="color:{};font-weight:600;">{}</span>',
            colors.get(obj.status, '#000'), obj.get_status_display())
    colored_status.short_description = 'Статус'

    def total_price_display(self, obj):
        return f'{obj.total_price()} руб.'
    total_price_display.short_description = 'Итоговая сумма'

    def summary_block(self, obj):
        if not obj or not obj.pk:
            return 'Сохраните корзину, чтобы увидеть итоги.'
        return format_html(
            '<div style="display:inline-block;padding:14px 20px;'
            'background:#f0f6ff;border:1px solid #c5dbff;border-radius:10px;'
            'font-size:14px;line-height:1.8;">'
            '<b>Суммарное количество единиц:</b> {}<br>'
            '<b>Итоговая стоимость:</b> {} руб.'
            '</div>',
            obj.total_quantity(), obj.total_price())
    summary_block.short_description = 'Итоги'
    class Media:
        css = {'all': ('store/cart_admin.css',)}
        js = ('store/cart_admin.js',)
