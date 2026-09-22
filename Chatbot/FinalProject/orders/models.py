from decimal import Decimal

from django.db import models
from django.conf import settings
from store.models import Product  # Links cleanly across to your store app

from django.db import models
from django.conf import settings
from store.models import Product

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_number = models.CharField(max_length=100, unique=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled & refund'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Remove shipping_cost field - we'll calculate it dynamically
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    shipping_address = models.TextField()
    billing_address = models.TextField()
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50, default='pending')
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        return sum(item.total for item in self.items.all())
    
    @property#@property turns a method into a virtual attribute that can be accessed like a field.
    def shipping_cost(self):
        """Calculate shipping cost based on address"""
        # Check if shipping address contains Dhaka
        if 'Dhaka' in self.shipping_address or 'dhaka' in self.shipping_address.lower():
            return Decimal('70.00')  # Inside Dhaka
        return Decimal('140.00')  # Outside Dhaka
    
    @property
    def total_amount(self):
        return (self.subtotal + self.tax + self.shipping_cost) - self.discount

    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(models.Model):
    """
    Weak entity representing individual lines items inside an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    # PROTECT ensures you cannot accidentally delete a product from your catalog
    # if a historical customer order requires it for accounting or sales reports.
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    
    # Captures the historic price snapshot at the exact millisecond of checkout
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('order', 'product')

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.order_number})"


class Payment(models.Model):
    """
    Weak entity matching 1:1 total participation with its parent Order.
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment',
        primary_key=True # Reuses the Order ID as its primary key to represent weak dependency
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order {self.order.order_number} - Status: {self.status}"


class Invoice(models.Model):
    """
    Weak entity matching 1:1 with Order; stores the file paths for your billing PDFs.
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='invoice',
        primary_key=True
    )
    invoice_number = models.CharField(max_length=100, unique=True)
    pdf_file = models.FileField(upload_to='invoices/') # File paths used by your custom admin generation tools
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_number}"