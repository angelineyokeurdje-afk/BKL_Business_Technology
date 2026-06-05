from django.contrib import admin
from .models import SecurityLog


@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display  = ('timestamp', 'user', 'action', 'ip', 'details')
    list_filter   = ('action',)
    search_fields = ('user__username', 'ip', 'details')
    readonly_fields = ('timestamp', 'user', 'action', 'ip', 'details')

    def has_add_permission(self, request):
        return False  # Les logs ne peuvent pas être ajoutés manuellement

    def has_change_permission(self, request, obj=None):
        return False  # Les logs sont en lecture seule
