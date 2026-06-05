"""
catalog/views.py
Vues pour le catalogue de produits et la page d'accueil.
"""

from django.shortcuts import render
from .models import Product, SiteSettings


# Fonctionnalités affichées sur la page d'accueil
FEATURES = [
    {
        'icon': 'bi bi-shield-check',
        'bg': 'linear-gradient(135deg,#4f46e5,#3730a3)',
        'title': 'Sécurité avancée',
        'desc': 'Vos données sont chiffrées et protégées contre les attaques — naviguez en toute sécurité.'
    },
    {
        'icon': 'bi bi-cart3',
        'bg': 'linear-gradient(135deg,#10b981,#059669)',
        'title': 'Commandes faciles',
        'desc': 'Ajoutez au panier, validez et suivez vos commandes en temps réel.'
    },
    {
        'icon': 'bi bi-people',
        'bg': 'linear-gradient(135deg,#f59e0b,#d97706)',
        'title': 'Multi-rôles',
        'desc': 'Clients, Vendeurs et Admins — chacun son espace et ses droits.'
    },
    {
        'icon': 'bi bi-code-slash',
        'bg': 'linear-gradient(135deg,#ef4444,#dc2626)',
        'title': 'API protégée',
        'desc': 'Endpoints JSON sécurisés par session — accès refusé sans authentification.'
    },
]


def index(request):
    """Page catalogue — liste de tous les produits."""
    products = Product.objects.all()
    return render(request, 'catalog/index.html', {
        'products': products
    })


def home(request):
    """Page d'accueil avec hero dynamique et features."""
    settings_site = SiteSettings.objects.first()
    return render(request, 'home.html', {
        'settings_site': settings_site,
        'features': FEATURES,
    })


def about(request):
    """Page À propos."""
    return render(request, 'about.html')