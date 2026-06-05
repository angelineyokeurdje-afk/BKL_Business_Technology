"""
bklbusiness/urls.py
Routage principal du projet BKLbusiness Service.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog import views as catalog_views

# ─── Personnalisation de l'interface admin ────────────────────────────────────
admin.site.site_header  = "BKLbusiness — Administration"
admin.site.site_title   = "BKLbusiness Admin"
admin.site.index_title  = "Tableau de bord"

urlpatterns = [
    # Interface d'administration Django
    path('admin/',      admin.site.urls),

    # Support multilingue
    path('i18n/',       include('django.conf.urls.i18n')),

    # Applications
    path('accounts/',   include('accounts.urls')),
    path('catalog/',    include('catalog.urls')),
    path('orders/',     include('orders.urls')),
    path('dashboard/',  include('dashboard.urls')),
    path('api/',        include('api.urls')),
    path('security/',   include('security.urls')),

    # Page d'accueil
    path('',            catalog_views.home, name='home'),
]

# ─── Servir les médias en développement uniquement ────────────────────────────
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)