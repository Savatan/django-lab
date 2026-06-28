# 📚 КнигоМир — Django-каталог книг

Учебный проект: каталог книг на Django с демонстрацией моделей, миграций,
наследования шаблонов и кастомных тегов/фильтров.

---

## Быстрый старт

```bash
# 1. Установить зависимости
pip install django

# 2. Применить миграции (создать таблицы в БД)
python manage.py migrate

# 3. Заполнить базу тестовыми данными
python manage.py shell < seed_data.py

# 4. Создать суперпользователя (для /admin/)
python manage.py createsuperuser

# 5. Запустить сервер
python manage.py runserver
```

Откройте: http://127.0.0.1:8000/

---

## Структура проекта

```
bookstore/
├── bookstore/                  # Конфигурация проекта
│   ├── settings.py             # Настройки Django
│   └── urls.py                 # Корневые URL
│
├── catalog/                    # Приложение каталога
│   ├── models.py               # ✅ МОДЕЛИ: Genre, Author, Book, Review
│   ├── views.py                # Представления (list, detail, authors)
│   ├── urls.py                 # URL-маршруты приложения
│   ├── admin.py                # Регистрация в админке
│   │
│   ├── migrations/
│   │   └── 0001_initial.py     # ✅ МИГРАЦИЯ: создание таблиц
│   │
│   ├── templatetags/
│   │   └── book_tags.py        # ✅ КАСТОМНЫЕ ТЕГИ И ФИЛЬТРЫ
│   │
│   └── templates/catalog/
│       ├── base.html           # ✅ БАЗОВЫЙ ШАБЛОН (родитель)
│       ├── _header.html        # ✅ {% include %}: шапка
│       ├── _footer.html        # ✅ {% include %}: подвал
│       ├── book_list.html      # ✅ {% extends %}: список книг
│       ├── book_detail.html    # ✅ {% extends %}: детальная страница
│       └── author_list.html    # ✅ {% extends %}: список авторов
│
├── seed_data.py                # Скрипт заполнения тестовыми данными
└── manage.py                   # Django management utility
```

---

## ✅ Модели (`catalog/models.py`)

| Модель   | Поля                                                   |
|----------|--------------------------------------------------------|
| `Genre`  | name, slug                                             |
| `Author` | first_name, last_name, birth_year, bio                 |
| `Book`   | title, author (FK), genres (M2M), description,         |
|          | published_year, pages, price, rating, status, cover_color |
| `Review` | book (FK), reviewer_name, score (1-5), text, created_at |

---

## ✅ Миграции (`catalog/migrations/0001_initial.py`)

Создаёт 4 таблицы + промежуточную таблицу для ManyToMany (Book ↔ Genre).

```bash
python manage.py makemigrations   # создать файл миграции
python manage.py migrate          # применить к БД
python manage.py showmigrations   # проверить статус
```

---

## ✅ Наследование шаблонов

### `{% extends %}` — вертикальное наследование

```
base.html  (родитель)
  ├── book_list.html    {% extends "catalog/base.html" %}
  ├── book_detail.html  {% extends "catalog/base.html" %}
  └── author_list.html  {% extends "catalog/base.html" %}
```

base.html определяет блоки:
```html
{% block title %}{% endblock %}
{% block content %}{% endblock %}
{% block extra_css %}{% endblock %}
```

Дочерние шаблоны их переопределяют:
```html
{% extends "catalog/base.html" %}
{% block title %}Каталог книг{% endblock %}
{% block content %}
  ... содержимое страницы ...
{% endblock %}
```

### `{% include %}` — включение частичных шаблонов

```html
{% include "catalog/_header.html" %}   {# шапка #}
{% include "catalog/_footer.html" %}   {# подвал #}
```

---

## ✅ Встроенные теги и фильтры Django (≥ 3 шт.)

| №  | Тег / Фильтр                        | Где используется       | Что делает                                |
|----|-------------------------------------|------------------------|-------------------------------------------|
| 1  | `{% for %}` / `{% empty %}`         | book_list, detail      | Итерация по queryset; вывод если пусто    |
| 2  | `{% if %}` / `{% elif %}` / `{% else %}` | все шаблоны       | Условная логика                           |
| 3  | `{% url 'name' %}` / `{% url 'name' pk %}` | все шаблоны    | Генерация URL по имени маршрута           |
| 4  | `{% now "Y" %}`                     | _footer.html           | Текущий год в копирайте                   |
| 5  | `{% with count=... %}{% endwith %}` | book_detail.html       | Локальная переменная в блоке              |
| 6  | `{% widthratio rating 5 100 %}`     | book_detail.html       | Вычисляет процент: (a/b)*c                |
| 7  | `{% block %}` / `{% endblock %}`    | base.html + дочерние   | Переопределяемые блоки                    |
| 8  | `{{ value\|floatformat:1 }}`        | book_list, detail      | Float с 1 знаком после запятой            |
| 9  | `{{ text\|truncatechars:40 }}`      | book_list.html         | Обрезка строки до N символов             |
| 10 | `{{ qs\|length }}`                  | book_list, authors     | Длина queryset / списка                   |
| 11 | `{{ dt\|date:"d F Y" }}`            | book_detail.html       | Форматирование даты                       |
| 12 | `{{ str\|slice:":1"\|upper }}`      | author_list.html       | Срез строки + в верхний регистр           |
| 13 | `{{ val\|default:"много" }}`        | _footer.html           | Значение по умолчанию если falsy          |

---

## ✅ Кастомные теги и фильтры (`catalog/templatetags/book_tags.py`)

### Простые теги (`simple_tag`)

| №  | Тег                              | Что делает                                    | Пример вывода                |
|----|----------------------------------|-----------------------------------------------|------------------------------|
| 1  | `{% site_name %}`                | Возвращает название сайта из константы        | `КнигоМир`                   |
| 2  | `{% star_rating 4.2 %}`          | HTML со звёздами ★/☆ и числом рейтинга        | `★★★★☆ (4.2)`               |
| 3  | `{% book_age 1951 %}`            | Возраст книги с правильным склонением         | `74 года назад`              |

### Фильтры (`filter`)

| №  | Фильтр                               | Что делает                                   | Пример                          |
|----|--------------------------------------|----------------------------------------------|---------------------------------|
| 1  | `{{ 1290\|rubles }}`                 | Форматирует цену в рублях                    | `1 290,00 ₽`                   |
| 2  | `{{ long_text\|short_description:90 }}` | Обрезает текст по границе слова + «…»     | `Первые 90 символов текста…`    |
| 3  | `{{ 'available'\|status_badge }}`    | HTML-бейдж с цветом по статусу              | `<span class="badge badge-green">В наличии</span>` |

### Подключение в шаблоне

```html
{% load book_tags %}

{# Теги #}
{% site_name %}
{% star_rating book.rating %}
{% book_age book.published_year %}

{# Фильтры #}
{{ book.price|rubles }}
{{ book.description|short_description:120 }}
{{ book.status|status_badge }}
```

---

## URL-маршруты

| URL                  | Имя                   | Представление       |
|----------------------|-----------------------|---------------------|
| `/`                  | `catalog:book_list`   | `views.book_list`   |
| `/book/<pk>/`        | `catalog:book_detail` | `views.book_detail` |
| `/authors/`          | `catalog:author_list` | `views.author_list` |
| `/admin/`            | —                     | Django Admin        |

---

## Страницы сайта

1. **Список книг** (`/`) — сетка карточек с фильтрацией по жанру и сортировкой
2. **Детальная страница** (`/book/<pk>/`) — полная информация, рейтинг-бар, отзывы
3. **Авторы** (`/authors/`) — карточки авторов с аватарами из инициалов
4. **Админка** (`/admin/`) — полное управление данными
