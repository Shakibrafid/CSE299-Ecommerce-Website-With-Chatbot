from rest_framework import viewsets, permissions
from backend.permissions import IsOwnerOrStaff, IsSupportAgentUser
from .models import ChatSession, ChatMessage, HumanSupportSession
from .serializers import ChatSessionSerializer, ChatMessageSerializer, HumanSupportSessionSerializer

class ChatSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_support_agent', False) or user.is_staff:
            return ChatSession.objects.filter(is_active=True)
        return ChatSession.objects.filter(user=user)

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_support_agent', False) or user.is_staff:
            return ChatMessage.objects.all()
        return ChatMessage.objects.filter(chat_session__user=user)
        

class HumanSupportSessionViewSet(viewsets.ModelViewSet):
    serializer_class = HumanSupportSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupportAgentUser]
    queryset = HumanSupportSession.objects.all()