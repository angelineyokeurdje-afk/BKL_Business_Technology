from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CatalogConfig(AppConfig):
    name = 'catalog'
    
    def ready(self):
        """Run when Django app is ready."""
        # Import here to avoid circular imports
        from .models import SiteSettings
        
        def create_default_sitesettings(sender, **kwargs):
            """
            Signal handler to create default SiteSettings after migrations.
            This ensures the record exists even if build.sh doesn't create it.
            """
            try:
                if not SiteSettings.objects.exists():
                    SiteSettings.objects.create(
                        hero_titre="Bienvenue sur BKLbusiness",
                        hero_description="Votre marketplace moderne et sécurisée. Découvrez des produits et services de qualité."
                    )
            except Exception:
                # Ignore if table doesn't exist yet
                pass
        
        # Connect signal to run after migrations
        post_migrate.connect(create_default_sitesettings, sender=self)
