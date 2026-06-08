"""
catalog/views.py
Vues pour le catalogue de produits et la page d'accueil.
"""

from django.shortcuts import render
from django.db import ProgrammingError, OperationalError
from .models import Product, SiteSettings


def get_site_settings():
    """
    Récupère les paramètres du site de manière sécurisée.
    Retourne None si la table n'existe pas encore (durant les migrations).
    """
    try:
        return SiteSettings.objects.first()
    except (ProgrammingError, OperationalError):
        # La table n'existe pas encore (migrations en cours ou première exécution)
        return None


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
    settings_site = get_site_settings()
    return render(request, 'home.html', {
        'settings_site': settings_site,
        'features': FEATURES,
    })


def about(request):
    """Page À propos avec présentation de la stack technique et sécurité."""

    # Technologies utilisées par la plateforme
    techs = [
        {'name': 'Django',     'role': 'Framework web',           'icon': 'bi bi-code-slash',   'color': '#092E20'},
        {'name': 'PostgreSQL', 'role': 'Base de données',          'icon': 'bi bi-database',     'color': '#336791'},
        {'name': 'Bootstrap',  'role': 'Interface utilisateur',    'icon': 'bi bi-layout-three-columns', 'color': '#7952B3'},
        {'name': 'Python',     'role': 'Langage backend',         'icon': 'bi bi-filetype-py',  'color': '#3776AB'},
        {'name': 'Cloudinary', 'role': 'Stockage médias',          'icon': 'bi bi-cloud-upload', 'color': '#3448C5'},
        {'name': 'Redis',      'role': 'Cache & sessions',         'icon': 'bi bi-database-gear','color': '#DC382D'},
        {'name': 'Docker',     'role': 'Conteneurisation',         'icon': 'bi bi-box-seam',     'color': '#2496ED'},
        {'name': 'Gunicorn',   'role': 'Serveur WSGI',            'icon': 'bi bi-server',       'color': '#499848'},
    ]

    # Mécanismes de sécurité implémentés
    security_items = [
        {'icon': 'bi bi-shield-lock',   'bg': '#4f46e5', 'title': 'CSRF & XSS',       'desc': 'Protection complète contre les attaques CSRF et XSS via Django.'},
        {'icon': 'bi bi-key',           'bg': '#10b981', 'title': 'Hash Argon2',       'desc': 'Mots de passe hashés avec Argon2, l\'algorithme le plus robuste.'},
        {'icon': 'bi bi-session',       'bg': '#f59e0b', 'title': 'Sessions sécurisées','desc': 'Sessions HTTP-only avec régénération à la connexion (anti-fixation).'},
        {'icon': 'bi bi-speedometer2',  'bg': '#ef4444', 'title': 'Rate Limiting',     'desc': 'Limitation des tentatives de connexion (brute-force protection).'},
        {'icon': 'bi bi-file-lock',     'bg': '#8b5cf6', 'title': 'Upload filtré',    'desc': 'Validation MIME, extension et taille pour tous les uploads.'},
        {'icon': 'bi bi-shield-check',  'bg': '#ec4899', 'title': 'Sanitization',     'desc': 'Nettoyage des entrées utilisateur avec Bleach (HTML/XSS).'},
    ]

    return render(request, 'about.html', {
        'techs': techs,
        'security_items': security_items,
    })
