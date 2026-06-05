"""
accounts/views.py
Authentification complète : inscription, connexion, déconnexion,
profil utilisateur, limitation des tentatives de connexion.
"""

import bleach
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from security.models import SecurityLog


# ─── Limite de tentatives de connexion ────────────────────────────────────────
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION   = 300  # 5 minutes en secondes


def _get_ip(request):
    """Extrait l'adresse IP réelle du client."""
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')


def _log(request, action, details=''):
    """Journalise une action de sécurité."""
    user = request.user if request.user.is_authenticated else None
    SecurityLog.objects.create(
        user=user,
        action=action,
        ip=_get_ip(request),
        details=details,
    )


def register(request):
    """Inscription d'un nouvel utilisateur avec validation complète."""

    if request.method == 'POST':

        # ─── Récupérer et sanitizer les données ──────────────────
        username  = bleach.clean(request.POST.get('username', '').strip())
        email     = bleach.clean(request.POST.get('email', '').strip())
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        role      = request.POST.get('role', 'client')

        # ─── Validation du nom d'utilisateur ─────────────────────
        if len(username) < 3 or len(username) > 30:
            messages.error(request, "Le nom doit faire entre 3 et 30 caractères.")
            return render(request, 'accounts/register.html')

        # ─── Validation de l'email ────────────────────────────────
        if '@' not in email or '.' not in email.split('@')[-1]:
            messages.error(request, "Adresse email invalide.")
            return render(request, 'accounts/register.html')

        # ─── Correspondance des mots de passe ────────────────────
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'accounts/register.html')

        # ─── Robustesse du mot de passe (Django validators) ──────
        try:
            validate_password(password1)
        except ValidationError as e:
            for err in e.messages:
                messages.error(request, err)
            return render(request, 'accounts/register.html')

        # ─── Unicité du nom d'utilisateur ────────────────────────
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, 'accounts/register.html')

        # ─── Unicité de l'email ───────────────────────────────────
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse email est déjà utilisée.")
            return render(request, 'accounts/register.html')

        # ─── Créer l'utilisateur (mot de passe hashé par Django) ─
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )

        # ─── Attribuer le rôle (seulement client ou vendeur) ─────
        if role in ('client', 'vendeur') and hasattr(user, 'profile'):
            user.profile.role = role
            user.profile.save()

        # ─── Envoi d'un email de bienvenue au client ────────────
        subject = 'Bienvenue sur BKLbusiness'
        message = (
            f'Bonjour {username},\n\n'
            'Merci pour votre inscription sur BKLbusiness.\n'
            'Votre compte a bien été créé et vous pouvez maintenant accéder à nos services.\n\n'
            'À bientôt sur BKLbusiness !\n'
        )
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'BKLbusiness <no-reply@example.com>')
        try:
            send_mail(subject, message, from_email, [email])
            _log(request, 'email_send', f"Email de bienvenue envoyé à : {email}")
        except Exception as exc:
            _log(request, 'email_error', f"Échec envoi email à {email} : {exc}")
            messages.warning(request, "Votre compte est créé, mais l'email de confirmation n'a pas pu être envoyé.")

        # ─── Journalisation ───────────────────────────────────────
        SecurityLog.objects.create(
            user=user,
            action='register',
            ip=_get_ip(request),
            details=f"Nouvel utilisateur : {username} ({role})"
        )

        # ─── Connexion automatique après inscription ──────────────
        login(request, user)
        messages.success(request, f"Bienvenue {username} ! Compte créé avec succès.")
        return redirect('catalog:index')

    return render(request, 'accounts/register.html')


def user_login(request):
    """Connexion avec limitation des tentatives (brute-force protection)."""

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # ─── Vérification du blocage en session ──────────────────
        attempts = request.session.get('login_attempts', 0)
        if attempts >= MAX_LOGIN_ATTEMPTS:
            _log(request, 'rate_limited', f"Trop de tentatives pour : {username}")
            messages.error(request,
                "Trop de tentatives de connexion. Veuillez patienter quelques minutes.")
            return render(request, 'accounts/login.html')

        # ─── Vérification des identifiants ───────────────────────
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Réinitialiser le compteur en cas de succès
            request.session['login_attempts'] = 0
            # Régénérer la session (contre session fixation)
            request.session.cycle_key()
            login(request, user)
            _log(request, 'login_ok', f"Connexion : {username}")
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('catalog:index')
        else:
            # Incrémenter le compteur de tentatives
            request.session['login_attempts'] = attempts + 1
            _log(request, 'login_fail', f"Échec de connexion : {username}")
            remaining = MAX_LOGIN_ATTEMPTS - (attempts + 1)
            return render(request, 'accounts/login.html', {
                'error': 'Identifiants incorrects.',
                'remaining': max(0, remaining),
            })

    return render(request, 'accounts/login.html')


def user_logout(request):
    """Déconnexion et destruction complète de la session."""
    username = request.user.username if request.user.is_authenticated else 'Anonyme'
    _log(request, 'logout', f"Déconnexion : {username}")
    request.session.flush()
    logout(request)
    messages.success(request, "Vous êtes bien déconnecté(e).")
    return redirect('login')


@login_required
def profile(request):
    """Affichage et modification du profil utilisateur."""
    user_profile = request.user.profile

    if request.method == 'POST':
        # ─── Sanitizer les données du profil ─────────────────────
        phone   = bleach.clean(request.POST.get('phone', '').strip())
        address = bleach.clean(request.POST.get('address', '').strip())
        first_name = bleach.clean(request.POST.get('first_name', '').strip())
        last_name  = bleach.clean(request.POST.get('last_name', '').strip())

        # ─── Validation du numéro de téléphone ────────────────────
        if phone and len(phone) > 20:
            messages.error(request, "Numéro de téléphone trop long.")
            return render(request, 'accounts/profile.html', {'profile': user_profile})

        # ─── Avatar (optionnel) ────────────────────────────────────
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            TYPES_OK = ['image/jpeg', 'image/png', 'image/webp']
            if avatar.content_type not in TYPES_OK:
                messages.error(request, "Format d'image non supporté (JPG, PNG, WebP uniquement).")
                return render(request, 'accounts/profile.html', {'profile': user_profile})
            if avatar.size > 2 * 1024 * 1024:
                messages.error(request, "L'image ne doit pas dépasser 2 Mo.")
                return render(request, 'accounts/profile.html', {'profile': user_profile})
            user_profile.avatar = avatar

        # ─── Sauvegarder ──────────────────────────────────────────
        user_profile.phone   = phone
        user_profile.address = address
        user_profile.save()

        request.user.first_name = first_name
        request.user.last_name  = last_name
        request.user.save()

        _log(request, 'profile_edit', "Modification du profil utilisateur")
        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'profile': user_profile})