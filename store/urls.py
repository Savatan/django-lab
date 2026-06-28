from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('carts/', views.cart_list, name='cart_list'),
]
