"""
Migration 0004: Create catalog_sitesettings table with raw SQL.

This migration uses raw SQL to reliably create the catalog_sitesettings table
for both PostgreSQL and SQLite. This is a fallback for migration 0003 which may
not have executed properly.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_fix_missing_sitesettings_table'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS catalog_sitesettings (
                id BIGSERIAL PRIMARY KEY,
                hero_image VARCHAR(100) NULL,
                hero_titre VARCHAR(200) NOT NULL,
                hero_description TEXT NOT NULL
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS catalog_sitesettings CASCADE;",
            state_operations=[],
        ),
    ]
