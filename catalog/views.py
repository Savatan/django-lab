from django.shortcuts import render, get_object_or_404
from .models import Book, Genre, Author


def book_list(request):
    """
    Список всех книг с фильтрацией по жанру.

    GET-параметры:
        genre (str): slug жанра для фильтрации
        sort  (str): поле сортировки (price, -price, rating, -rating, title)
    """
    books = Book.objects.select_related('author').prefetch_related('genres').all()
    genres = Genre.objects.all()

    # Фильтрация по жанру
    genre_slug = request.GET.get('genre', '')
    active_genre = None
    if genre_slug:
        active_genre = Genre.objects.filter(slug=genre_slug).first()
        if active_genre:
            books = books.filter(genres=active_genre)

    # Сортировка
    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = {
        'price': 'price',
        '-price': '-price',
        'rating': '-rating',   # сначала высокий рейтинг
        'title': 'title',
        'year': '-published_year',
    }
    books = books.order_by(allowed_sorts.get(sort, '-created_at'))

    context = {
        'books': books,
        'genres': genres,
        'active_genre': active_genre,
        'current_sort': sort,
        'total_books': books.count(),
    }
    return render(request, 'catalog/book_list.html', context)


def book_detail(request, pk):
    """Детальная страница книги с отзывами."""
    book = get_object_or_404(
        Book.objects.select_related('author').prefetch_related('genres', 'reviews'),
        pk=pk,
    )
    reviews = book.reviews.all()

    context = {
        'book': book,
        'reviews': reviews,
        'reviews_count': reviews.count(),
    }
    return render(request, 'catalog/book_detail.html', context)


def author_list(request):
    """Список авторов с количеством их книг."""
    authors = Author.objects.prefetch_related('books').all()
    context = {'authors': authors}
    return render(request, 'catalog/author_list.html', context)
