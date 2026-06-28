from django.db import models


class Customer(models.Model):
    """Покупатель."""
    name = models.CharField('Имя', max_length=150)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    registered_at = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар."""
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    in_stock = models.BooleanField('В наличии', default=True)
    created_at = models.DateTimeField('Добавлен', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.price} руб.)'


class Cart(models.Model):
    """Корзина: покупатель + товары через промежуточную модель CartItem."""

    STATUS_NEW = 'new'
    STATUS_PAID = 'paid'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_PAID, 'Оплачена'),
        (STATUS_CANCELLED, 'Отменена'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
        related_name='carts',
    )
    products = models.ManyToManyField(
        Product,
        through='CartItem',
        verbose_name='Товары',
        related_name='carts',
        blank=True,
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-created_at']

    def __str__(self):
        return f'Корзина #{self.pk} — {self.customer.name}'

    def total_quantity(self):
        """Суммарное количество единиц товара в корзине."""
        return sum(item.quantity for item in self.items.all())
    total_quantity.short_description = 'Кол-во единиц'

    def total_price(self):
        """Итоговая стоимость корзины."""
        return sum(item.product.price * item.quantity for item in self.items.all())
    total_price.short_description = 'Итоговая сумма'


class CartItem(models.Model):
    """Промежуточная модель: товар в корзине и его количество."""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name='Корзина',
        related_name='items',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция корзины'
        verbose_name_plural = 'Позиции корзины'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def subtotal(self):
        """Стоимость позиции: цена × количество."""
        return self.product.price * self.quantity
    subtotal.short_description = 'Подытог'
