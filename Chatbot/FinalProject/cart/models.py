from django.db import models
from django.conf import settings
from store.models import Product  # Importing Product from your store app

class Cart(models.Model):
    # Weak entity 1:1 total participation with User
    # null=True, blank=True allows guest shoppers to have a cart before registering
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True
    )
    
    # Used to track anonymous guest carts 
    # unique=True ensures one guest session can only ever have one active cart record
    session_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart for User: {self.user.username}"
        if self.session_id:
            return f"Guest Cart: {self.session_id[:8]}"
        return "Guest Cart"


class CartItem(models.Model):
    """
    A weak entity representing items added to a cart. 
    Maintains unique per composite constraints to avoid duplicate product rows in the same cart.
    """
    # Identifying relationship: A CartItem cannot exist without a parent Cart
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    # References Product: Many-to-One total participation from CartItem side
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    
    quantity = models.PositiveIntegerField(default=1)
    
    # Captures a historical snapshot of the price at the exact moment the item was added
    price_at_add = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Implements "Unique per composite" from your ER diagram documentation.
        # This prevents the database from creating two distinct rows for the same product in one cart.
        # Instead, your logic will find the row and increment the quantity.
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart #{self.cart.id}"