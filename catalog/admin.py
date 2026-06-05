from django.contrib import admin
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
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Empêche la suppression du seul paramètre du site
        return False