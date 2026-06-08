"""
Migration 0004: Create catalog_sitesettings table with raw SQL.

This migration uses raw SQL to reliably create the catalog_sitesettings table
for both PostgreSQL and SQLite. Uses CREATE TABLE IF NOT EXISTS to be idempotent.
"""

from django.db import migrations


def create_table_postgresql(apps, schema_editor):
    """Create table for PostgreSQL."""
    schema_editor.execute("""
        CREATE TABLE IF NOT EXISTS catalog_sitesettings (
            id BIGSERIAL PRIMARY KEY,
            hero_image VARCHAR(100) NULL,
            hero_titre VARCHAR(200) NOT NULL,
            hero_description TEXT NOT NULL
        );
    """)


def create_table_sqlite(apps, schema_editor):
    """Create table for SQLite."""
    schema_editor.execute("""
        CREATE TABLE IF NOT EXISTS catalog_sitesettings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hero_image VARCHAR(100) NULL,
            hero_titre VARCHAR(200) NOT NULL,
            hero_description TEXT NOT NULL
        );
    """)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_fix_missing_sitesettings_table'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                # PostgreSQL path
                """
                CREATE TABLE IF NOT EXISTS catalog_sitesettings (
                    id BIGSERIAL PRIMARY KEY,
                    hero_image VARCHAR(100) NULL,
                    hero_titre VARCHAR(200) NOT NULL,
                    hero_description TEXT NOT NULL
                );
                """,
            ],
            reverse_sql="DROP TABLE IF EXISTS catalog_sitesettings CASCADE;",
            state_operations=[],
        ),
    ]
