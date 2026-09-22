from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    created_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='created_users'
    )
    # Removed the redundant username field entirely because AbstractUser handles it perfectly
    
    # Keeping email here because you added unique=True (AbstractUser doesn't enforce uniqueness by default)
    email = models.EmailField(unique=True) 
    
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_guest = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    # Ensures your app uses the unique email for registration logic if desired
    REQUIRED_FIELDS = ['email'] 


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
    )
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username}"