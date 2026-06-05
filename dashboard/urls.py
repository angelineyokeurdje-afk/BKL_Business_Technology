"""
dashboard/urls.py
Routes du tableau de bord administrateur.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',        views.dashboard_home,    name='dashboard'),
    path('users/',  views.user_list,         name='dashboard_users'),
    path('orders/', views.order_management,  name='dashboard_orders'),
]
