"""
seed_data.py — Скрипт наполнения базы тестовыми данными
=========================================================
Запуск:
    python manage.py shell < seed_data.py
или:
    python manage.py runscript seed_data   (если установлен django-extensions)
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from catalog.models import Genre, Author, Book, Review

# Чистим старые данные (для повторного запуска)
Review.objects.all().delete()
Book.objects.all().delete()
Author.objects.all().delete()
Genre.objects.all().delete()

# ── Жанры ────────────────────────────────────────────────────────────────
genres_data = [
    ('Классика', 'classics'),
    ('Фантастика', 'sci-fi'),
    ('Детектив', 'detective'),
    ('Роман', 'novel'),
    ('Философия', 'philosophy'),
    ('Программирование', 'programming'),
]
genres = {}
for name, slug in genres_data:
    g = Genre.objects.create(name=name, slug=slug)
    genres[slug] = g
print(f'Создано жанров: {len(genres)}')

# ── Авторы ───────────────────────────────────────────────────────────────
authors_data = [
    ('Лев', 'Толстой', 1828,
     'Один из величайших писателей мировой литературы. Автор романов «Война и мир», «Анна Каренина».'),
    ('Фёдор', 'Достоевский', 1821,
     'Классик русской литературы, мастер психологического романа. «Преступление и наказание», «Идиот».'),
    ('Айзек', 'Азимов', 1920,
     'Американский писатель-фантаст, автор «Foundation» и «Я, Робот». Популяризатор науки.'),
    ('Агата', 'Кристи', 1890,
     'Королева детектива. Создала Эркюля Пуаро и мисс Марпл. Рекордсмен по тиражам среди детективщиков.'),
    ('Роберт', 'Мартин', 1952,
     'Дядя Боб. Автор книг по чистому коду и гибкой разработке программного обеспечения.'),
]
authors = {}
for first, last, year, bio in authors_data:
    a = Author.objects.create(first_name=first, last_name=last, birth_year=year, bio=bio)
    authors[last] = a
print(f'Создано авторов: {len(authors)}')

# ── Книги ─────────────────────────────────────────────────────────────────
books_data = [
    {
        'title': 'Война и мир',
        'author': authors['Толстой'],
        'genres': [genres['classics'], genres['novel']],
        'description': (
            'Эпический роман, охватывающий события наполеоновских войн в России. '
            'История нескольких аристократических семей на фоне исторических '
            'потрясений начала XIX века. Масштабное полотно человеческих судеб, '
            'любви, войны и философских исканий.'
        ),
        'published_year': 1869,
        'pages': 1274,
        'price': 890.00,
        'rating': 4.8,
        'status': 'available',
        'cover_color': '#8B1A1A',
    },
    {
        'title': 'Преступление и наказание',
        'author': authors['Достоевский'],
        'genres': [genres['classics'], genres['novel']],
        'description': (
            'Психологический роман о студенте Раскольникове, совершившем убийство '
            'и переживающем муки совести. Глубокое исследование природы преступления, '
            'вины и искупления. Один из ключевых текстов мировой литературы.'
        ),
        'published_year': 1866,
        'pages': 671,
        'price': 650.00,
        'rating': 4.7,
        'status': 'available',
        'cover_color': '#2C3E50',
    },
    {
        'title': 'Основание',
        'author': authors['Азимов'],
        'genres': [genres['sci-fi']],
        'description': (
            'Первая книга легендарной серии «Foundation». История учёного Гэри '
            'Селдона, разработавшего «психоисторию» — науку предсказания будущего '
            'цивилизаций. Он пытается сохранить знания человечества перед крахом '
            'Галактической Империи.'
        ),
        'published_year': 1951,
        'pages': 244,
        'price': 720.00,
        'rating': 4.6,
        'status': 'available',
        'cover_color': '#16537E',
    },
    {
        'title': 'Убийство в Восточном экспрессе',
        'author': authors['Кристи'],
        'genres': [genres['detective']],
        'description': (
            'Эркюль Пуаро, возвращаясь из Стамбула, оказывается в поезде с убитым '
            'пассажиром. Все подозреваемые — попутчики вагона. Блестящий образец '
            'классического детектива с неожиданной развязкой.'
        ),
        'published_year': 1934,
        'pages': 256,
        'price': 580.00,
        'rating': 4.5,
        'status': 'available',
        'cover_color': '#8E6B2E',
    },
    {
        'title': 'Чистый код',
        'author': authors['Мартин'],
        'genres': [genres['programming']],
        'description': (
            'Практическое руководство по написанию читаемого, поддерживаемого кода. '
            'Роберт Мартин делится принципами, паттернами и практиками, '
            'позволяющими писать профессиональный код. Обязательная книга '
            'для каждого разработчика.'
        ),
        'published_year': 2008,
        'pages': 431,
        'price': 1290.00,
        'rating': 4.4,
        'status': 'available',
        'cover_color': '#1B5E20',
    },
    {
        'title': 'Я, Робот',
        'author': authors['Азимов'],
        'genres': [genres['sci-fi'], genres['philosophy']],
        'description': (
            'Сборник рассказов, объединённых темой искусственного интеллекта. '
            'Азимов формулирует знаменитые Три закона роботехники и исследует '
            'их последствия в разнообразных сюжетных ситуациях. Основа '
            'современной НФ об ИИ.'
        ),
        'published_year': 1950,
        'pages': 224,
        'price': 680.00,
        'rating': 4.5,
        'status': 'out_of_stock',
        'cover_color': '#37474F',
    },
    {
        'title': 'Анна Каренина',
        'author': authors['Толстой'],
        'genres': [genres['classics'], genres['novel']],
        'description': (
            'Трагическая история замужней женщины, полюбившей блестящего офицера '
            'Вронского. Роман о свободе и долге, страсти и общественных условностях, '
            'написанный с потрясающей психологической глубиной.'
        ),
        'published_year': 1878,
        'pages': 864,
        'price': 790.00,
        'rating': 4.7,
        'status': 'coming_soon',
        'cover_color': '#880E4F',
    },
    {
        'title': 'Архитектура программного обеспечения',
        'author': authors['Мартин'],
        'genres': [genres['programming']],
        'description': (
            'Книга об архитектуре ПО: принципы SOLID, компонентная модель, '
            'архитектурные паттерны и границы систем. Мартин объясняет, как '
            'проектировать системы, которые легко поддерживать и расширять.'
        ),
        'published_year': 2017,
        'pages': 432,
        'price': 1450.00,
        'rating': 4.3,
        'status': 'available',
        'cover_color': '#004D40',
    },
]

for data in books_data:
    book_genres = data.pop('genres')
    book = Book.objects.create(**data)
    book.genres.set(book_genres)

print(f'Создано книг: {Book.objects.count()}')

# ── Отзывы ───────────────────────────────────────────────────────────────
war_peace = Book.objects.get(title='Война и мир')
clean_code = Book.objects.get(title='Чистый код')
foundation = Book.objects.get(title='Основание')

reviews_data = [
    (war_peace, 'Мария С.', 5, 'Шедевр на все времена! Читала три раза и каждый раз открываю что-то новое.'),
    (war_peace, 'Алексей П.', 4, 'Огромный роман, но стоит каждой страницы. Батальные сцены — нечто особенное.'),
    (clean_code, 'Дмитрий К.', 5, 'Изменила моё отношение к профессии. Теперь код пишу совсем иначе.'),
    (clean_code, 'Светлана Т.', 4, 'Очень полезная книга, особенно для тех, кто работает в команде.'),
    (foundation, 'Игорь В.', 5, 'Азимов создал целую вселенную с нуля. Грандиозная идея — психоистория!'),
]

for book, name, score, text in reviews_data:
    Review.objects.create(book=book, reviewer_name=name, score=score, text=text)

print(f'Создано отзывов: {Review.objects.count()}')
print('\n✅ База данных успешно заполнена!')
print('Запустите сервер: python manage.py runserver')
