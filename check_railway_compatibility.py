#!/usr/bin/env python
"""
Railway Deployment Compatibility Checker for BKLbusiness

This script verifies that your Django application is properly configured
for deployment on Railway.
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed."""
    required_packages = {
        'django': 'django',
        'gunicorn': 'gunicorn',
        'psycopg2': 'psycopg2',
        'dj_database_url': 'dj_database_url',
        'whitenoise': 'whitenoise',
        'pillow': 'PIL',  # Pillow imports as PIL
    }
    
    missing = []
    for display_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(display_name)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        return False
    print("✅ All required packages installed")
    return True


def check_settings():
    """Check Django settings for production readiness."""
    BASE_DIR = Path(__file__).resolve().parent
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bklbusiness.settings')
    
    try:
        import django
        django.setup()
        from django.conf import settings
        
        issues = []
        
        # Check DEBUG
        if settings.DEBUG and os.environ.get('RAILWAY_ENVIRONMENT'):
            issues.append("DEBUG is True in production!")
        
        # Check SECRET_KEY
        if not os.environ.get('DJANGO_SECRET_KEY') and os.environ.get('RAILWAY_ENVIRONMENT'):
            issues.append("DJANGO_SECRET_KEY not set in production")
        
        # Check ALLOWED_HOSTS
        if not settings.ALLOWED_HOSTS and os.environ.get('RAILWAY_ENVIRONMENT'):
            issues.append("ALLOWED_HOSTS is empty in production")
        elif '.railway.app' not in str(settings.ALLOWED_HOSTS) and os.environ.get('RAILWAY_ENVIRONMENT'):
            issues.append("ALLOWED_HOSTS doesn't include .railway.app")
        
        # Check database config
        if not settings.DATABASES.get('default'):
            issues.append("No default database configured")
        
        # Check STATIC files
        if not settings.STATIC_ROOT:
            issues.append("STATIC_ROOT not configured")
        
        if not settings.STATIC_URL:
            issues.append("STATIC_URL not configured")
        
        # Check WSGI app
        wsgi_app = settings.WSGI_APPLICATION
        if not wsgi_app:
            issues.append("WSGI_APPLICATION not configured")
        
        if issues:
            print("❌ Settings issues found:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        
        print("✅ Django settings properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Error checking settings: {e}")
        return False


def check_files():
    """Check if required files exist."""
    BASE_DIR = Path(__file__).resolve().parent
    required_files = {
        'runtime.txt': 'Python version specification',
        'requirements.txt': 'Python dependencies',
        'Procfile': 'Process types',
        'railway.json': 'Railway configuration',
        'build.sh': 'Build script',
        '.env.example': 'Environment variables template',
        'bklbusiness/settings.py': 'Django settings',
        'bklbusiness/wsgi.py': 'WSGI application',
        'manage.py': 'Django management',
    }
    
    missing = []
    for file_path, description in required_files.items():
        full_path = BASE_DIR / file_path
        if not full_path.exists():
            missing.append(f"{file_path} ({description})")
    
    if missing:
        print("❌ Missing required files:")
        for file in missing:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True


def check_runtime():
    """Check Python runtime version."""
    BASE_DIR = Path(__file__).resolve().parent
    runtime_file = BASE_DIR / 'runtime.txt'
    
    if runtime_file.exists():
        with open(runtime_file) as f:
            version = f.read().strip()
        
        # Check if version is stable (3.9+, not beta)
        if 'python-3' in version:
            try:
                minor = version.split('-')[1].split('.')[1]
                if minor in ['14', '15', '20', '30']:  # Beta versions
                    print(f"⚠️  Python version {version} might be unstable")
                    return True
            except:
                pass
        
        print(f"✅ Python runtime: {version}")
        return True
    
    print("❌ runtime.txt not found")
    return False


def check_env_vars():
    """Check if environment variables are set."""
    required_vars = {
        'production': ['DJANGO_SECRET_KEY', 'RAILWAY_ENVIRONMENT'],
        'optional': ['EMAIL_HOST_USER', 'CLOUDINARY_CLOUD_NAME'],
    }
    
    is_prod = bool(os.environ.get('RAILWAY_ENVIRONMENT'))
    
    if is_prod:
        missing = []
        for var in required_vars['production']:
            if not os.environ.get(var):
                missing.append(var)
        
        if missing:
            print(f"❌ Missing environment variables: {', '.join(missing)}")
            return False
        
        print("✅ All required environment variables set")
    else:
        print("ℹ️  Development mode - skipping production env var checks")
    
    return True


def main():
    """Run all checks."""
    print("\n" + "="*60)
    print("Railway Deployment Compatibility Checker")
    print("="*60 + "\n")
    
    checks = [
        ("Python Packages", check_requirements),
        ("Project Files", check_files),
        ("Runtime Version", check_runtime),
        ("Django Settings", check_settings),
        ("Environment Variables", check_env_vars),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error during {name} check: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Your application is ready for Railway deployment!")
        return 0
    else:
        print("\n⚠️  Please fix the issues above before deploying to Railway")
        return 1


if __name__ == '__main__':
    sys.exit(main())
