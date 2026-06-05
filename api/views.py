"""
api/views.py
Endpoints API JSON protégés par authentification.
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from catalog.models import Product
from orders.models import Order


def _require_auth(request):
    """Retourne une réponse 401 si l'utilisateur n'est pas authentifié."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentification requise.'}, status=401)
    return None


@require_GET
@login_required
def api_profile(request):
    """
    GET /api/profile/
    Retourne les informations du profil de l'utilisateur connecté.
    """
    profile = getattr(request.user, 'profile', None)
    data = {
        'id':         request.user.id,
        'username':   request.user.username,
        'email':      request.user.email,
        'first_name': request.user.first_name,
        'last_name':  request.user.last_name,
        'role':       profile.role if profile else 'client',
        'is_staff':   request.user.is_staff,
    }
    return JsonResponse(data)


@require_GET
@login_required
def api_products(request):
    """
    GET /api/products/
    Retourne la liste des produits en JSON.
    Accès refusé sans authentification.
    """
    products = Product.objects.values(
        'id', 'name', 'description', 'price', 'created_at'
    )
    return JsonResponse({'products': list(products), 'count': products.count()})


@require_GET
@login_required
def api_orders(request):
    """
    GET /api/orders/
    Retourne les commandes de l'utilisateur connecté en JSON.
    Les admins voient toutes les commandes.
    """
    if request.user.is_staff:
        orders_qs = Order.objects.select_related('user').order_by('-created_at')
    else:
        orders_qs = Order.objects.filter(user=request.user).order_by('-created_at')

    data = []
    for order in orders_qs:
        data.append({
            'id':         order.id,
            'user':       order.user.username,
            'status':     order.status,
            'status_label': order.get_status_display(),
            'total':      str(order.total_price()),
            'created_at': order.created_at.isoformat(),
        })

    return JsonResponse({'orders': data, 'count': len(data)})
