"""
security/views.py
Formulaire de contact, upload sécurisé et journal de sécurité.
"""

import os
import bleach
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import SecurityLog


def _get_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')


def contact(request):
    """Formulaire de contact sécurisé avec sanitization bleach."""

    if request.method == 'POST':
        nom     = bleach.clean(request.POST.get('nom', '').strip())
        email   = bleach.clean(request.POST.get('email', '').strip())
        sujet   = bleach.clean(request.POST.get('sujet', '').strip())
        message = bleach.clean(request.POST.get('message', '').strip())

        # ─── Validations ──────────────────────────────────────────
        if len(nom) < 2:
            messages.error(request, "Le nom doit faire au moins 2 caractères.")
            return render(request, 'security/contact.html')

        if '@' not in email or '.' not in email.split('@')[-1]:
            messages.error(request, "Adresse email invalide.")
            return render(request, 'security/contact.html')

        if len(sujet) < 3:
            messages.error(request, "Le sujet doit faire au moins 3 caractères.")
            return render(request, 'security/contact.html')

        if len(message) < 10:
            messages.error(request, "Le message doit faire au moins 10 caractères.")
            return render(request, 'security/contact.html')

        # ─── Journalisation ───────────────────────────────────────
        user = request.user if request.user.is_authenticated else None
        SecurityLog.objects.create(
            user=user,
            action='login_ok',  # Réutilisé comme "action neutre"
            ip=_get_ip(request),
            details=f"Contact de {nom} <{email}> — Sujet : {sujet}"
        )

        messages.success(request, "✅ Message envoyé avec succès ! Nous vous répondrons rapidement.")
        return render(request, 'security/contact.html')

    return render(request, 'security/contact.html')


def upload(request):
    """Formulaire d'upload de fichier avec contrôles stricts."""

    TYPES_AUTORISES = ['image/jpeg', 'image/png', 'application/pdf']
    EXTENSIONS_OK   = ['.jpg', '.jpeg', '.png', '.pdf']
    TAILLE_MAX      = 2 * 1024 * 1024  # 2 Mo

    if request.method == 'POST':
        fichier = request.FILES.get('fichier')

        if not fichier:
            messages.error(request, "Aucun fichier sélectionné.")
            return render(request, 'security/upload.html')

        # ─── Vérification du type MIME ────────────────────────────
        if fichier.content_type not in TYPES_AUTORISES:
            messages.error(request,
                f"Type non autorisé : {fichier.content_type}. Formats acceptés : JPG, PNG, PDF.")
            return render(request, 'security/upload.html')

        # ─── Vérification de l'extension ─────────────────────────
        ext = os.path.splitext(fichier.name)[1].lower()
        if ext not in EXTENSIONS_OK:
            messages.error(request,
                f"Extension non autorisée : {ext}. Acceptées : .jpg, .png, .pdf")
            return render(request, 'security/upload.html')

        # ─── Vérification de la taille ────────────────────────────
        if fichier.size > TAILLE_MAX:
            messages.error(request,
                f"Fichier trop volumineux : {fichier.size / 1024 / 1024:.1f} Mo (max 2 Mo).")
            return render(request, 'security/upload.html')

        # ─── Journalisation ───────────────────────────────────────
        user = request.user if request.user.is_authenticated else None
        SecurityLog.objects.create(
            user=user,
            action='upload',
            ip=_get_ip(request),
            details=f"Upload : {fichier.name} ({fichier.size / 1024:.1f} Ko)"
        )

        messages.success(request,
            f"✅ Fichier « {fichier.name} » uploadé avec succès ({fichier.size / 1024:.1f} Ko).")
        return render(request, 'security/upload.html')

    return render(request, 'security/upload.html')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login/')
def security_logs(request):
    """Journal de sécurité — accessible uniquement aux administrateurs."""
    logs = SecurityLog.objects.select_related('user').order_by('-timestamp')[:200]
    return render(request, 'security/logs.html', {'logs': logs})
