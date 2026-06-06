#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Appliquer les migrations
python manage.py migrate

# 3. Créer le superutilisateur automatiquement s'il n'existe pas
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@bkl.com', 'MonMotDePasse123!')"
