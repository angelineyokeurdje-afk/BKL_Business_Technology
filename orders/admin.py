from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = 'Sous-total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter   = ('status',)
    search_fields = ('user__username',)
    inlines       = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')
