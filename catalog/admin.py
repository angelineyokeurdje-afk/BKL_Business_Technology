from django.contrib import admin
from django.db import ProgrammingError, OperationalError
from .models import Product, SiteSettings


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'price', 'created_at']
    search_fields = ['name', 'description']
    list_filter   = ['created_at']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['hero_titre', 'hero_description']

    def has_add_permission(self, request):
        # Interdit de créer une 2e instance si une existe déjà
        try:
            return not SiteSettings.objects.exists()
        except (ProgrammingError, OperationalError):
            # Table doesn't exist yet (migrations in progress)
            return False

    def has_delete_permission(self, request, obj=None):
        # Empêche la suppression du seul paramètre du site
        return False