"""
accounts/models.py
Modèle UserProfile avec gestion des rôles utilisateurs.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Profil étendu lié à chaque utilisateur Django."""

    ROLE_CHOICES = [
        ('client',  'Client'),
        ('vendeur', 'Vendeur'),
        ('admin',   'Administrateur'),
    ]

    user      = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role      = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone     = models.CharField(max_length=20, blank=True, default='')
    address   = models.TextField(blank=True, default='')
    avatar    = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def is_admin(self):
        return self.role == 'admin' or self.user.is_staff

    def is_vendeur(self):
        return self.role == 'vendeur'

    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'


# ─── Signal : création automatique du profil lors de la création d'un User ───
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un UserProfile à la création d'un User."""
    if created:
        role = 'admin' if instance.is_staff else 'client'
        UserProfile.objects.create(user=instance, role=role)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil quand l'utilisateur est sauvegardé."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
