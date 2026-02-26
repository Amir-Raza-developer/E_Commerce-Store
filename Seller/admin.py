from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model  = OrderItem
    extra  = 0
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display   = ['id', 'buyer', 'full_name', 'total', 'status', 'payment_method', 'created_at']
    list_filter    = ['status', 'payment_method']
    search_fields  = ['buyer__username', 'full_name', 'email']
    list_editable  = ['status']
    readonly_fields = ['buyer', 'created_at']
    inlines        = [OrderItemInline]

    def has_add_permission(self, request):
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
