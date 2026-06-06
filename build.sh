#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Installation des dépendances
pip install -r requirements.txt

# 2. Collecte des fichiers statiques
python manage.py collectstatic --no-input

# 3. Application des migrations
python manage.py migrate

# 4. Création sécurisée du superutilisateur sans doublon
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='BRUNO').exists():
    User.objects.create_superuser('BRUNO', 'bklbusinesstechnologies@gmail.com', 'bkl@-25')
    print('Superutilisateur créé avec succès !')
else:
    print('Le superutilisateur existe déjà.')
"