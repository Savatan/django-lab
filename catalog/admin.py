from django.contrib import admin
from .models import Book, Author, Genre, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'birth_year']
    search_fields = ['last_name', 'first_name']


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_year', 'price', 'rating', 'status']
    list_filter = ['status', 'genres', 'published_year']
    search_fields = ['title', 'author__last_name']
    filter_horizontal = ['genres']
    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'reviewer_name', 'score', 'created_at']
