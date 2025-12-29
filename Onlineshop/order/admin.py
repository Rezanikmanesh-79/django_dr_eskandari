from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # readonly_fields = ('product', 'quantity', 'price', 'weight', 'get_cost', 'get_weight', 'get_post_cost')
    can_delete = False
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',  'first_name', 'last_name', 'email',
                    'phone', 'created_at', 'paid', 'payment_code', 'get_total_cost')
    list_filter = ('paid', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email',
                     'phone', 'address', 'payment_code')
    inlines = [OrderItemInline]

    ordering = ('-created_at',)
    # show_change_link = True
