"""
orders/urls.py
Routes pour le panier et les commandes.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('cart/',                    views.cart,             name='cart'),
    path('cart/add/<int:product_id>/',    views.add_to_cart,  name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/',                views.checkout,         name='checkout'),
    path('my-orders/',               views.order_list,       name='order_list'),
    path('my-orders/<int:pk>/',      views.order_detail,     name='order_detail'),
]
