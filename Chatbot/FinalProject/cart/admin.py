from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    """
    Allows you to view, add, or remove items directly 
    inside the main Cart details page.
    """
    model = CartItem
    extra = 0
    fields = ['product', 'quantity', 'price_at_add']
    readonly_fields = ['price_at_add']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # Added 'id' and 'session_id' so guest carts are instantly recognizable
    list_display = ['id', 'display_owner', 'session_id', 'item_count', 'created_at', 'updated_at']
    
    # Added 'session_id' to search so you can find a cart using a guest token
    search_fields = ['user__username', 'user__email', 'session_id']
    
    readonly_fields = ['created_at', 'updated_at']
    
    # Embeds the items table directly inside the Cart page
    inlines = [CartItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Number of Items"

    def display_owner(self, obj):
        """Displays the username if it belongs to a user, otherwise labels it a Guest."""
        if obj.user:
            return f"👤 {obj.user.username}"
        return "🌐 Guest Shopper"
    display_owner.short_description = "Cart Owner"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    # Organizes item listings cleanly
    list_display = ['id', 'cart', 'product', 'quantity', 'price_at_add', 'created_at']
    list_editable = ['quantity']  # Allows quick quantity adjustments right from the list view
    search_fields = ['product__name', 'cart__session_id', 'cart__user__username']
    readonly_fields = ['created_at', 'updated_at']