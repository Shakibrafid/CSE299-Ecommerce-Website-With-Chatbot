from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Profile

# Inline setup so you can view and edit the user's address/picture directly on their User page!
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile Info'
    fk_name = 'user'

    '''User Admin Page           Profile Admin Page
┌─────────────────┐      ┌─────────────────┐
│ User: John      │      │ Profile: John   │
│ Username: john  │      │ Address: 123 St │
│ Email: john@... │      │ City: New York  │
│ [Save]          │      │ [Save]          │
└─────────────────┘      └─────────────────┘
    ↑                            ↑
    └── You have to go here ─────┘
    
    
    User Admin Page
┌─────────────────────────────────────────┐
│ User: John                              │
│ Username: john                          │
│ Email: john@email.com                   │
│                                          │
│ ┌─────────────────────────────────────┐ │
│ │ Profile Info                        │ │
│ │ Address: 123 Main St                │ │
│ │ City: New York                      │ │
│ │ State: NY                           │ │
│ │ Zip: 10001                          │ │
│ └─────────────────────────────────────┘ │
│                                          │
│ [Save]  [Delete]                        │
└─────────────────────────────────────────┘'''

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'is_customer', 'is_guest', 'is_active']
    list_filter = ['is_customer', 'is_guest', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'phone']
    ordering = ['username']
    
    # Embed profile edits directly into the user screen
    inlines = [ProfileInline]
    
    # Form layout for EDITING an existing user
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('phone', 'is_guest', 'is_customer', 'created_by'),
        }),
    )
    
    # Form layout for CREATING a brand new user (Fixes the admin crash)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('email', 'phone', 'is_guest', 'is_customer', 'created_by'),
        }),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'state', 'country', 'created_at']
    list_filter = ['city', 'state', 'country']
    search_fields = ['user__username', 'user__email', 'city']
    readonly_fields = ['created_at', 'updated_at']