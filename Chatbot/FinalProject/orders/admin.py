# orders/admin.py
from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from .models import Order
from billing.views import admin_invoice_pdf_view  # Ensure this view function exists

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Added 'print_bill_action' column to the very front of your display list
    list_display = [
        'print_bill_action',
        'order_number',
        'user',
        'subtotal',
        'shipping_cost',
        'tax',
        'discount',
        'total_amount',
        'status',
        'created_at'
    ]
    
    # Appended 'print_bill_action' to readonly_fields so it displays inside the detail view too
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'subtotal', 'shipping_cost', 'total_amount', 'print_bill_action']
    
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Financial', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total_amount')
        }),
        ('Addresses', {
            'fields': ('shipping_address', 'billing_address')
        }),
        ('Payment', {
            'fields': ('payment_method',)
        }),
        ('Additional', {
            'fields': ('notes', 'created_at', 'updated_at', 'print_bill_action')  # Visible at bottom of detail block
        }),
    )

    def get_urls(self):
        """
        Dynamically registers the internal admin URL pattern for generating billing papers.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:order_id>/print-bill-pdf/',
                self.admin_site.admin_view(admin_invoice_pdf_view),
                name='admin-order-invoice-pdf',
            ),
        ]
        return custom_urls + urls

    def print_bill_action(self, obj):
        """
        Generates a clean HTML print link action button for the list table dashboard rows.
        """
        if obj.id:
            url = reverse('admin:admin-order-invoice-pdf', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" target="_blank" style="background-color: #417690; color: white; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-weight: bold; white-space: nowrap;">🖨️ Print Bill</a>',
                url
            )
        return ""
        
    print_bill_action.short_description = 'Billing'
