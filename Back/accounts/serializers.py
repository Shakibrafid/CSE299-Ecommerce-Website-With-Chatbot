from rest_framework import serializers
from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'profile_picture']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True) # Nesting the profile information inside the user JSON

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'is_customer', 'is_guest', 'profile']