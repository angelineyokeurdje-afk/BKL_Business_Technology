#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Installation des dépendances
pip install -r requirements.txt

# 2. Application des migrations de base de données
python manage.py migrate

# 3. Initialiser les paramètres du site par défaut
python manage.py shell -c "
from catalog.models import SiteSettings;
if not SiteSettings.objects.exists():
    SiteSettings.objects.create(
        hero_titre='Bienvenue sur BKLbusiness',
        hero_description='Votre marketplace moderne et sécurisée. Découvrez des produits et services de qualité.'
    );
    print('✓ Paramètres du site créés avec succès !')
else:
    print('✓ Paramètres du site déjà existants.')
"

# 4. Collecte des fichiers statiques
python manage.py collectstatic --no-input

# 5. Création sécurisée du superutilisateur via variables d'environnement uniquement
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model;
User = get_user_model();
admin_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin');
admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '');
admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '');
if admin_password and not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(admin_username, admin_email, admin_password)
    print(f'✓ Superutilisateur \"{admin_username}\" créé avec succès !')
elif admin_password:
    print(f'✓ Le superutilisateur \"{admin_username}\" existe déjà.')
else:
    print('ℹ Aucun superutilisateur créé. Définissez DJANGO_SUPERUSER_PASSWORD dans l\\'environnement.')
"
