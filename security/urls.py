"""
security/urls.py
Routes pour le contact, l'upload et le journal de sécurité.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact,       name='contact'),
    path('upload/',  views.upload,        name='upload'),
    path('logs/',    views.security_logs, name='security_logs'),
]