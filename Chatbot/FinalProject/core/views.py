from rest_framework import viewsets, permissions
from backend.permissions import IsOwnerOrStaff
from .models import Setting, Notification
from .serializers import SettingSerializer, NotificationSerializer

class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        # Notifications must remain confidential to the target account
        return Notification.objects.filter(user_id=self.request.user)