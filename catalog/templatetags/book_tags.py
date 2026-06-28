
from django import template
from django.utils.html import format_html, mark_safe
from datetime import date

register = template.Library()

SITE_TITLE = 'КнигоМир'


@register.simple_tag
def site_name():
   
    return SITE_TITLE


@register.simple_tag
def star_rating(rating):
    
    try:
        rating = float(rating)
    except (TypeError, ValueError):
        rating = 0.0

    full_stars = int(rating)                
    empty_stars = 5 - full_stars           

    stars_html = '★' * full_stars + '☆' * empty_stars

    rating_str = f'{rating:.1f}'
    return format_html(
        '<span class="stars" title="Рейтинг {}/5">{}</span>'
        '<span class="rating-num">({})</span>',
        rating_str, stars_html, rating_str,
    )


@register.simple_tag
def book_age(published_year):
    
    try:
        years = date.today().year - int(published_year)
    except (TypeError, ValueError):
        return mark_safe('<span class="book-age">—</span>')

    if years == 0:
        label = 'В этом году'
    elif years == 1:
        label = '1 год назад'
    elif 2 <= years <= 4:
        label = f'{years} года назад'
    else:
        label = f'{years} лет назад'

    return format_html('<span class="book-age">{}</span>', label)



@register.filter(name='rubles')
def rubles(value):
   
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return value

    integer_part = int(amount)
    decimal_part = round((amount - integer_part) * 100)

    formatted_int = f'{integer_part:,}'.replace(',', '\u00a0')  # неразрывный пробел

    return mark_safe(f'{formatted_int},{decimal_part:02d}\u00a0₽')


@register.filter(name='short_description')
def short_description(text, max_length=150):
 
    if not text:
        return ''
    text = str(text)
    if len(text) <= max_length:
        return text
    # Обрезаем по границе слова, чтобы не разрывать слово
    truncated = text[:max_length].rsplit(' ', 1)[0]
    return truncated + '…'


@register.filter(name='status_badge')
def status_badge(status):
   
    badges = {
        'available':    ('badge-green', 'В наличии'),
        'out_of_stock': ('badge-red',   'Нет в наличии'),
        'coming_soon':  ('badge-blue',  'Скоро в продаже'),
    }
    css_class, label = badges.get(status, ('badge-gray', status))
    return format_html(
        '<span class="badge {}">{}</span>',
        css_class, label,
    )
