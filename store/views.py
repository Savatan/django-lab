from django.shortcuts import render
from .models import Cart


def cart_list(request):
    """Страница /carts/ — список всех корзин."""
    carts = (
        Cart.objects
        .select_related('customer')
        .prefetch_related('products')
        .all()
    )
    context = {
        'carts': carts,
        'total_carts': carts.count(),
    }
    return render(request, 'store/cart_list.html', context)
