"""
bklbusiness/settings.py
Configuration Django sécurisée pour BKLbusiness Service.
Optimisé pour la sécurité, les performances et la production.
"""

from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

# ─── Chemins de base ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Mode debug ───────────────────────────────────────────────────────────────
DEBUG = os.environ.get('DJANGO_DEBUG', '').strip().lower() in ('1', 'true', 'yes')
_IN_PRODUCTION = bool(
    os.environ.get('RENDER', '')
    or os.environ.get('RAILWAY_ENVIRONMENT', '')
    or os.environ.get('RAILWAY_SERVICE_ID', '')
)

# ─── Sécurité : clé secrète ───────────────────────────────────────────────────
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if _IN_PRODUCTION:
        raise ValueError("DJANGO_SECRET_KEY environment variable is required in production!")
    # Use a fallback insecure key only in development
    SECRET_KEY = 'django-insecure-%0&#^1-(*vitnwrz6iw!s*)n^!zj4@^l8r**d$j)ghw^%po&lu'

ALLOWED_HOSTS = [
    'localhost', '127.0.0.1',
    '.railway.app', '.render.com',
    'bkl-business-technology.onrender.com',
    os.environ.get('ALLOWED_HOST', '').strip(),
    os.environ.get('RAILWAY_PUBLIC_DOMAIN', '').strip(),
]
ALLOWED_HOSTS = [h for h in ALLOWED_HOSTS if h]

# ─── Applications installées ──────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    # Applications internes
    'accounts',
    'catalog',
    'orders',
    'dashboard',
    'api',
    'security',
]

# ─── Middleware ───────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bklbusiness.urls'

# ─── Templates ────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bklbusiness.wsgi.application'

# ─── Base de données ─────────────────────────────────────────────────────────
# En production (Render/Railway), utilise PostgreSQL via nBASE_URL
# En local, utilise SQLite (aucune installation requise)
db_url = os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_URL_PRIMARY')

if db_url:
    # PostgreSQL via DATABASE_URL (production)
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(
                db_url, conn_max_age=600, ssl_require=True
            )
        }
    except Exception:
        # Fallback configuration - all values must come from environment
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DB_NAME', ''),
                'USER': os.environ.get('DB_USER', ''),
                'PASSWORD': os.environ.get('DB_PASSWORD', ''),
                'HOST': os.environ.get('DB_HOST', ''),
                'PORT': os.environ.get('DB_PORT', '5432'),
                'CONN_MAX_AGE': int(os.environ.get('DB_CONN_MAX_AGE', '600')),
            }
        }
else:
    # SQLite en local (développement)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ─── Cache ────────────────────────────────────────────────────────────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'bklbusiness-cache',
    }
}

# Utiliser Redis / Memcached si disponible via variable d'environnement
REDIS_URL = os.environ.get('REDIS_URL', '')
if REDIS_URL:
    try:
        CACHES['default'] = {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
        }
    except Exception:
        pass

# ─── Hashage des mots de passe ────────────────────────────────────────────────
AUTH_PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# ─── Validateurs de mots de passe ─────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internationalisation ─────────────────────────────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE     = 'Africa/Douala'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

LANGUAGES = [
    ('fr', _('Français')),
    ('en', _('English')),
    ('ar', _('العربية')),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

# ─── Fichiers statiques ───────────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─── Fichiers médias ──────────────────────────────────────────────────────────
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── Clé primaire par défaut ──────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Sécurité des sessions (production) ──────────────────────────────────────
SESSION_COOKIE_HTTPONLY         = True
SESSION_COOKIE_SECURE           = bool(_IN_PRODUCTION)
SESSION_COOKIE_SAMESITE         = 'Strict' if _IN_PRODUCTION else 'Lax'
SESSION_COOKIE_AGE              = 1800  # 30 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST      = True

# ─── Protection CSRF ──────────────────────────────────────────────────────────
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE   = bool(_IN_PRODUCTION)
CSRF_COOKIE_SAMESITE = 'Strict' if _IN_PRODUCTION else 'Lax'

# ─── En-têtes de sécurité (production uniquement) ────────────────────────────
X_FRAME_OPTIONS                = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF    = True
SECURE_BROWSER_XSS_FILTER      = True
SECURE_SSL_REDIRECT            = bool(_IN_PRODUCTION)
SECURE_PROXY_SSL_HEADER        = ('HTTP_X_FORWARDED_PROTO', 'https') if _IN_PRODUCTION else None
SECURE_HSTS_SECONDS            = 31536000 if _IN_PRODUCTION else 0      # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = bool(_IN_PRODUCTION)
SECURE_HSTS_PRELOAD            = bool(_IN_PRODUCTION)

# ─── Redirections après authentification ──────────────────────────────────────
LOGIN_URL           = '/accounts/login/'
LOGIN_REDIRECT_URL  = '/catalog/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ─── Configuration Email ──────────────────────────────────────────────────────
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'true').lower() in ('1', 'true', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL',
    f'BKLbusiness <{EMAIL_HOST_USER or "no-reply@example.com"}>'
)

# ─── Cloudinary (optionnel) ──────────────────────────────────────────────────
USE_CLOUDINARY = os.environ.get('USE_CLOUDINARY', '') in ('1', 'true', 'True') or bool(os.environ.get('CLOUDINARY_URL'))

if USE_CLOUDINARY:
    try:
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api

        cloudinary.config(
            cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
            api_key    = os.environ.get('CLOUDINARY_API_KEY', ''),
            api_secret = os.environ.get('CLOUDINARY_API_SECRET', ''),
            secure     = True
        )

        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    except Exception:
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ─── Django REST Framework (si utilisé) ──────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
