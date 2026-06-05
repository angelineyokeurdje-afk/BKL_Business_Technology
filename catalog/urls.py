"""
catalog/urls.py
Routes pour le catalogue de produits.
"""

from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('',       views.index, name='index'),
    path('about/', views.about, name='about'),
]