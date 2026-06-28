from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    """Жанр книги."""
    name = models.CharField('Название жанра', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    """Автор книги."""
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    birth_year = models.PositiveSmallIntegerField('Год рождения', null=True, blank=True)
    bio = models.TextField('Биография', blank=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    """Книга каталога."""

    STATUS_AVAILABLE = 'available'
    STATUS_OUT_OF_STOCK = 'out_of_stock'
    STATUS_COMING_SOON = 'coming_soon'

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'В наличии'),
        (STATUS_OUT_OF_STOCK, 'Нет в наличии'),
        (STATUS_COMING_SOON, 'Скоро в продаже'),
    ]

    title = models.CharField('Название', max_length=255)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='books',
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='books',
        blank=True,
    )
    description = models.TextField('Описание')
    published_year = models.PositiveSmallIntegerField('Год издания')
    pages = models.PositiveSmallIntegerField('Количество страниц')
    price = models.DecimalField('Цена (руб.)', max_digits=8, decimal_places=2)
    rating = models.FloatField(
        'Рейтинг',
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE,
    )
    created_at = models.DateTimeField('Добавлена', auto_now_add=True)
    cover_color = models.CharField(
        'Цвет обложки (HEX)',
        max_length=7,
        default='#4A90D9',
        help_text='Например: #4A90D9',
    )

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']

    def __str__(self):
        return f'"{self.title}" — {self.author}'

    @property
    def is_available(self):
        return self.status == self.STATUS_AVAILABLE

    @property
    def rating_stars(self):
        """Возвращает количество полных звёзд (0–5)."""
        return int(round(self.rating))


class Review(models.Model):
    """Отзыв на книгу."""
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name='Книга',
        related_name='reviews',
    )
    reviewer_name = models.CharField('Имя читателя', max_length=100)
    score = models.PositiveSmallIntegerField(
        'Оценка (1-5)',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв {self.reviewer_name} на «{self.book.title}»'
