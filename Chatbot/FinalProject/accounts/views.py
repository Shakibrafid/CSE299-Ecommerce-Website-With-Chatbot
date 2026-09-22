from rest_framework import viewsets, permissions, generics
from backend.permissions import IsOwnerOrStaff

from .models import User, Profile
from .serializers import (
    ProfileSerializer,
    RegisterSerializer,
    UserSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]

        return [
            permissions.IsAuthenticated(),
            IsOwnerOrStaff()
        ]