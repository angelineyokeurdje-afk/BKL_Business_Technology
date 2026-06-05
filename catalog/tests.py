"""
catalog/urls.py
URLs du catalogue
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',      views.index, name='catalog'),
    path('home/', views.index, name='home'),
]
