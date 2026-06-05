"""
orders/models.py
Modèles pour le panier et la gestion des commandes.
"""

from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product


class Order(models.Model):
    """Commande passée par un utilisateur."""

    STATUS_CHOICES = [
        ('pending',    'En attente'),
        ('confirmed',  'Confirmée'),
        ('shipped',    'Expédiée'),
        ('delivered',  'Livrée'),
        ('cancelled',  'Annulée'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status      = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    notes       = models.TextField(blank=True, default='', verbose_name='Notes')

    def total_price(self):
        """Calcule le prix total de la commande."""
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Commande #{self.pk} — {self.user.username} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-created_at']


class OrderItem(models.Model):
    """Ligne d'article dans une commande."""

    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=2)  # Prix au moment de la commande

    def subtotal(self):
        """Sous-total de cette ligne."""
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    class Meta:
        verbose_name = 'Article commandé'
        verbose_name_plural = 'Articles commandés'
