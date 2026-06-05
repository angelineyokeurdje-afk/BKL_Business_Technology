"""
api/urls.py
Routes des endpoints API protégés.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('profile/',  views.api_profile,  name='api_profile'),
    path('products/', views.api_products, name='api_products'),
    path('orders/',   views.api_orders,   name='api_orders'),
]