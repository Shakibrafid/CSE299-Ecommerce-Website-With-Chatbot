from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Self-referencing foreign key for hierarchical nesting (subcategories)
    # Both sides are partial participation, so null=True and blank=True are required
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )
    
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    # Total participation from Product side: Every product MUST belong to a category
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Financial fields should always use DecimalField to protect monetary precision
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/main/', blank=True, null=True) # Base image
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    Supplemental model resolving the multi-valued 'images' attribute on Product.
    Enforces a Many-to-One relationship back to the main Product record.
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='products/gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gallery Image for {self.product.name}"


class Inventory(models.Model):
    """
    A transaction ledger logging every change made to stock levels.
    """
    # Total participation from Inventory side: An entry must map to a product
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='inventory_logs'
    )
    
    # Tracks both additions (+10 for restock) and subtractions (-2 for damaged goods)
    quantity_change = models.IntegerField() 
    reason = models.CharField(max_length=255) # e.g., 'Restock', 'Damaged', 'Audit adjustment'
    note = models.TextField(blank=True, null=True)
    
    # Partial participation from both sides: The modifier can be null if automated (e.g. system sales)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='inventory_adjustments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    #related_name decides what you call the “list of connected objects” from the other side.
    class Meta:
        verbose_name_plural = "Inventory Logs"

    def __str__(self):
        sign = "+" if self.quantity_change >= 0 else ""
        return f"{self.product.name}: {sign}{self.quantity_change} ({self.reason})"
    '''quantity_change = 5 → +5
quantity_change = -2 → -2'''