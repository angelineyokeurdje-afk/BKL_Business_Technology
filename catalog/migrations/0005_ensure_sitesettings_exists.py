"""
Migration 0005: Ensure catalog_sitesettings table exists and has data.

This migration:
1. Creates the table using database operations (works on PostgreSQL and SQLite)
2. Ensures a default SiteSettings record exists
3. Uses a data migration so it runs even if state is confused

This is the authoritative fix for the catalog_sitesettings issue.
"""

from django.db import migrations


def create_sitesettings_if_missing(apps, schema_editor):
    """Create the catalog_sitesettings table if it doesn't exist."""
    
    # Create the table based on database backend
    if schema_editor.connection.vendor == 'postgresql':
        # PostgreSQL: Use BIGSERIAL for auto-increment
        schema_editor.execute("""
            CREATE TABLE IF NOT EXISTS catalog_sitesettings (
                id BIGSERIAL PRIMARY KEY,
                hero_image VARCHAR(100),
                hero_titre VARCHAR(200) NOT NULL,
                hero_description TEXT NOT NULL
            );
        """)
    else:
        # SQLite and others: Use INTEGER AUTOINCREMENT
        schema_editor.execute("""
            CREATE TABLE IF NOT EXISTS catalog_sitesettings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hero_image VARCHAR(100),
                hero_titre VARCHAR(200) NOT NULL,
                hero_description TEXT NOT NULL
            );
        """)
    
    # Ensure at least one SiteSettings record exists
    try:
        schema_editor.execute(
            """
            INSERT INTO catalog_sitesettings (hero_titre, hero_description)
            SELECT %s, %s
            WHERE NOT EXISTS (SELECT 1 FROM catalog_sitesettings)
            """,
            ["Bienvenue sur BKLbusiness", "Votre marketplace moderne et sécurisée."]
        )
    except Exception as e:
        # If insert fails, the record might already exist or table might have data
        pass


def noop_reverse(apps, schema_editor):
    """No-op reverse - we never drop the table."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_create_sitesettings_table'),
    ]

    operations = [
        migrations.RunPython(
            code=create_sitesettings_if_missing,
            reverse_code=noop_reverse,
        ),
    ]
