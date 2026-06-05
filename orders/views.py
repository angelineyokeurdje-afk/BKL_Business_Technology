"""
orders/views.py
Gestion du panier (session), validation de commande et suivi.
"""

import bleach
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product
from .models import Order, OrderItem
from security.models import SecurityLog


def _get_ip(request):
    """Extrait l'IP réelle du client."""
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')


@login_required
def cart(request):
    """Affiche le panier stocké en session."""
    cart_data = request.session.get('cart', {})
    items = []
    total = 0

    for product_id, qty in cart_data.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            subtotal = product.price * qty
            total += subtotal
            items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass

    return render(request, 'orders/cart.html', {
        'cart_items': items,
        'total': total,
    })


@login_required
def add_to_cart(request, product_id):
    """Ajoute un produit au panier (stocké en session)."""
    product = get_object_or_404(Product, pk=product_id)

    cart = request.session.get('cart', {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart

    messages.success(request, f"« {product.name} » ajouté au panier.")
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    """Retire un produit du panier."""
    cart = request.session.get('cart', {})
    key = str(product_id)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        messages.info(request, "Article retiré du panier.")
    return redirect('cart')


@login_required
def checkout(request):
    """Convertit le panier en commande confirmée."""
    cart_data = request.session.get('cart', {})

    if not cart_data:
        messages.warning(request, "Votre panier est vide.")
        return redirect('cart')

    if request.method == 'POST':
        notes = bleach.clean(request.POST.get('notes', ''))

        # Créer la commande
        order = Order.objects.create(user=request.user, status='pending', notes=notes)

        for product_id, qty in cart_data.items():
            try:
                product = Product.objects.get(pk=int(product_id))
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price,
                )
            except Product.DoesNotExist:
                pass

        # Vider le panier
        request.session['cart'] = {}

        # Journaliser la commande
        SecurityLog.objects.create(
            user=request.user,
            action='order',
            ip=_get_ip(request),
            details=f"Commande #{order.pk} — Total : {order.total_price()} FCFA"
        )

        messages.success(request, f"Commande #{order.pk} validée avec succès !")
        return redirect('order_detail', pk=order.pk)

    # Préparer un récapitulatif pour la page checkout
    items = []
    total = 0
    for product_id, qty in cart_data.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            subtotal = product.price * qty
            total += subtotal
            items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass

    return render(request, 'orders/checkout.html', {
        'cart_items': items,
        'total': total,
    })


@login_required
def order_list(request):
    """Liste des commandes de l'utilisateur connecté."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    """Détail d'une commande (accessible uniquement par le propriétaire ou un admin)."""
    order = get_object_or_404(Order, pk=pk)

    # Vérification du droit d'accès
    if order.user != request.user and not request.user.is_staff:
        SecurityLog.objects.create(
            user=request.user,
            action='access_denied',
            ip=_get_ip(request),
            details=f"Tentative d'accès à la commande #{pk}"
        )
        messages.error(request, "Vous n'avez pas accès à cette commande.")
        return redirect('order_list')

    return render(request, 'orders/order_detail.html', {'order': order})
