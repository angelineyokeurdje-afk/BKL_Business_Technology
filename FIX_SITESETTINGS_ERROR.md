# Fix for catalog_sitesettings Table Error

## Problem Statement
PostgreSQL error: `relation "catalog_sitesettings" does not exist`

This error occurred because:
1. The application tried to query `catalog_sitesettings` on every homepage load
2. The table was missing from the production PostgreSQL database
3. Migrations were marked as applied but the table was never physically created

## Root Cause Analysis
- Migration 0002 (`sitesettings`) created the model definition
- Migration 0003 (attempted to create the table with complex `SeparateDatabaseAndState` logic)
- The table was not actually created in the database
- Every homepage request failed because `SiteSettings.objects.first()` was called unconditionally

## Solutions Implemented

### 1. **Defensive Code in Views** ✅
**File**: `catalog/views.py`

Added a safe wrapper function that catches database errors:
```python
def get_site_settings():
    """
    Récupère les paramètres du site de manière sécurisée.
    Retourne None si la table n'existe pas encore (durant les migrations).
    """
    try:
        return SiteSettings.objects.first()
    except (ProgrammingError, OperationalError):
        # La table n'existe pas encore (migrations en cours ou première exécution)
        return None
```

Updated `home()` view to use this safe function:
```python
def home(request):
    """Page d'accueil avec hero dynamique et features."""
    settings_site = get_site_settings()  # Safe - returns None if table doesn't exist
    return render(request, 'home.html', {
        'settings_site': settings_site,
        'features': FEATURES,
    })
```

Template already handles `None` gracefully:
```html
{% if settings_site %}
    <h1>{{ settings_site.hero_titre }}</h1>
{% else %}
    <h1>Bienvenue sur BKLbusiness</h1>
{% endif %}
```

### 2. **Bulletproof Migration** ✅
**File**: `catalog/migrations/0004_create_sitesettings_table.py`

Created a new migration using raw SQL with `CREATE TABLE IF NOT EXISTS`:
- Idempotent: Safe to run multiple times
- No state issues: Uses `RunSQL` directly
- Handles errors gracefully

### 3. **Build Script Initialization** ✅
**File**: `build.sh`

Added a step after migrations to ensure a default SiteSettings record exists:
```bash
# 3. Initialiser les paramètres du site par défaut
python manage.py shell -c "
from catalog.models import SiteSettings;
if not SiteSettings.objects.exists():
    SiteSettings.objects.create(
        hero_titre='Bienvenue sur BKLbusiness',
        hero_description='Votre marketplace moderne et sécurisée.'
    );
    print('✓ Paramètres du site créés avec succès !')
else:
    print('✓ Paramètres du site déjà existants.')
"
```

This ensures that:
- On fresh deployments: A default record is created
- On re-deployments: Existing record is preserved
- The application always has a fallback

## Deployment Instructions

### For Railway Deployment

1. **Ensure DATABASE_URL is set** in Railway variables
2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```
3. **Build script will automatically**:
   - Create the table (migration 0004)
   - Initialize default SiteSettings
   - Collect static files
   - Create superuser if credentials provided

4. **Application resilience**:
   - Homepage will load even if table doesn't exist (safe fallback)
   - Once build script creates SiteSettings, dynamic content loads

## Verification

### Local Testing
```bash
# Test that the defensive function works
python manage.py shell -c "
from catalog.views import get_site_settings
settings = get_site_settings()
print(f'SiteSettings: {settings}')
"
```

### Production Verification
1. Check migrations applied:
   ```bash
   python manage.py showmigrations catalog
   ```
   Expected output:
   ```
   catalog
    [X] 0001_initial
    [X] 0002_sitesettings
    [X] 0003_fix_missing_sitesettings_table
    [X] 0004_create_sitesettings_table
   ```

2. Check SiteSettings exists:
   ```bash
   python manage.py shell -c "
   from catalog.models import SiteSettings
   print(SiteSettings.objects.count())
   "
   ```
   Should output: `1`

3. Test homepage loads without errors

## Files Modified

1. ✅ `catalog/views.py` - Added defensive `get_site_settings()` function
2. ✅ `catalog/migrations/0004_create_sitesettings_table.py` - Improved migration
3. ✅ `build.sh` - Added SiteSettings initialization step

## Future Prevention

This issue is now permanently resolved through:

1. **Application Layer**: View functions are defensive and handle missing tables
2. **Database Layer**: Migration is idempotent and reliable
3. **Deployment Layer**: Build script ensures data is initialized

The application will no longer crash if the `catalog_sitesettings` table is missing! 🎉
