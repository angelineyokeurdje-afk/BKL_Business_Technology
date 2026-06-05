"""
dashboard/views.py
Tableau de bord administrateur — accès réservé au personnel (is_staff).
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from catalog.models import Product
from orders.models import Order
from security.models import SecurityLog


def staff_required(view_func):
    """Décorateur : redirige si l'utilisateur n'est pas staff."""
    decorated = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='/accounts/login/'
    )(view_func)
    return decorated


@login_required
@staff_required
def dashboard_home(request):
    """Vue principale du tableau de bord admin."""

    # Statistiques générales
    total_users    = User.objects.count()
    total_products = Product.objects.count()
    total_orders   = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()

    # Dernières commandes
    recent_orders  = Order.objects.select_related('user').order_by('-created_at')[:10]

    # Derniers logs de sécurité
    recent_logs    = SecurityLog.objects.select_related('user').order_by('-timestamp')[:20]

    # Répartition des commandes par statut
    status_stats = {
        'pending':   Order.objects.filter(status='pending').count(),
        'confirmed': Order.objects.filter(status='confirmed').count(),
        'shipped':   Order.objects.filter(status='shipped').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }

    context = {
        'total_users':    total_users,
        'total_products': total_products,
        'total_orders':   total_orders,
        'pending_orders': pending_orders,
        'recent_orders':  recent_orders,
        'recent_logs':    recent_logs,
        'status_stats':   status_stats,
    }

    return render(request, 'dashboard/home.html', context)


@login_required
@staff_required
def user_list(request):
    """Liste de tous les utilisateurs (admin only)."""
    users = User.objects.select_related('profile').order_by('-date_joined')
    return render(request, 'dashboard/user_list.html', {'users': users})


@login_required
@staff_required
def order_management(request):
    """Gestion de toutes les commandes (admin only)."""
    orders = Order.objects.select_related('user').order_by('-created_at')
    return render(request, 'dashboard/orders.html', {'orders': orders})
