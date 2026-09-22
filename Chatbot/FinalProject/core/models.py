from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

'''Setting Table:
# Add a setting
Setting.objects.create(
    key='CURRENCY_SYMBOL',
    value='$',
    description='Currency symbol on prices'
)

Setting.objects.create(
    key='TAX_RATE',
    value='0.10',
    description='Sales tax rate (10%)'
)

Setting.objects.create(
    key='COMPANY_NAME',
    value='My E-commerce Store',
    description='Company name displayed on site'
)'''

class Setting(models.Model):
    """
    Standalone configuration management entity with zero relational weights.
    """
    # Alternate Key: e.g., 'MAINTENANCE_MODE' or 'CURRENCY_SYMBOL'
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


class Notification(models.Model):
    """
    Weak Entity belonging to User via an asymmetric M:1 relationship mapping.
    """
    # Total participation from Notification side: A notification must belong to someone.
    # Note: Handled as standard ForeignKey (M:1) rather than unique OneToOne,
    # so a single user can have an infinite feed of unique alerts.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50) # e.g., 'order_status', 'chat_alert', 'system'
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"