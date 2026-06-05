"""
security/models.py
Modèle SecurityLog pour la journalisation des actions sensibles.
"""

from django.db import models
from django.contrib.auth.models import User


class SecurityLog(models.Model):
    """Journal des événements de sécurité de l'application."""

    ACTION_CHOICES = [
        ('login_ok',      'Connexion réussie'),
        ('login_fail',    'Tentative de connexion échouée'),
        ('logout',        'Déconnexion'),
        ('register',      'Inscription'),
        ('pw_reset',      'Réinitialisation mot de passe'),
        ('upload',        'Upload de fichier'),
        ('order',         'Commande passée'),
        ('profile_edit',  'Modification du profil'),
        ('access_denied', 'Accès refusé'),
        ('rate_limited',  'Trop de tentatives'),
    ]

    user      = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='security_logs', verbose_name='Utilisateur'
    )
    action    = models.CharField(max_length=20, choices=ACTION_CHOICES)
    ip        = models.GenericIPAddressField(null=True, blank=True, verbose_name='Adresse IP')
    details   = models.TextField(blank=True, default='', verbose_name='Détails')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Date/Heure')

    def __str__(self):
        username = self.user.username if self.user else 'Anonyme'
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {username} — {self.get_action_display()}"

    class Meta:
        verbose_name = 'Journal de sécurité'
        verbose_name_plural = 'Journaux de sécurité'
        ordering = ['-timestamp']
