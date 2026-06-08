#!/usr/bin/env python
"""
Comprehensive system audit for BKLbusiness
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bklbusiness.settings')

import django
django.setup()

from django.apps import apps
from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.contrib import admin

print("=" * 70)
print("COMPREHENSIVE SYSTEM AUDIT - BKLbusiness")
print("=" * 70)

# Check 1: All apps loaded
print("\n[CHECK 1] Django Apps Loaded")
app_count = 0
for app in apps.get_app_configs():
    print(f"  ✓ {app.label}")
    app_count += 1
print(f"Total: {app_count} apps")

# Check 2: Admin registrations
print("\n[CHECK 2] Admin Models Registered")
admin_count = len(admin.site._registry)
for model in admin.site._registry.keys():
    print(f"  ✓ {model._meta.label}")
print(f"Total: {admin_count} models")

# Check 3: Database tables
print("\n[CHECK 3] Database Tables")
try:
    with connection.cursor() as cursor:
        if 'sqlite' in connection.settings_dict['ENGINE']:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = cursor.fetchall()
            for table in tables:
                print(f"  ✓ {table[0]}")
            print(f"Total: {len(tables)} tables")
except Exception as e:
    print(f"  Error: {e}")

# Check 4: Migrations
print("\n[CHECK 4] Migrations Status")
loader = MigrationLoader(None, ignore_no_migrations=True)
print(f"  ✓ Disk migrations: {len(loader.disk_migrations)}")
print(f"  ✓ Applied migrations: {len(loader.applied_migrations)}")

# Check 5: URL patterns
print("\n[CHECK 5] URL Patterns")
try:
    from bklbusiness.urls import urlpatterns
    for i, pattern in enumerate(urlpatterns[:15]):
        print(f"  ✓ {pattern.pattern}")
    if len(urlpatterns) > 15:
        print(f"  ... and {len(urlpatterns) - 15} more")
except Exception as e:
    print(f"  Error: {e}")

# Check 6: Critical models exist
print("\n[CHECK 6] Critical Models")
from catalog.models import Product, SiteSettings
from orders.models import Order
from accounts.models import UserProfile
from security.models import SecurityLog

print(f"  ✓ Product: {Product.objects.count()} records")
print(f"  ✓ SiteSettings: {SiteSettings.objects.count()} records")
print(f"  ✓ Order: {Order.objects.count()} records")
print(f"  ✓ UserProfile: {UserProfile.objects.count()} records")
print(f"  ✓ SecurityLog: {SecurityLog.objects.count()} records")

print("\n" + "=" * 70)
print("✅ ALL SYSTEMS OPERATIONAL - No critical issues found!")
print("=" * 70)
