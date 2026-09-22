import uuid

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
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


class AIChatAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        message_text = request.data.get('message')
        if not message_text:
            return Response({'detail': 'Missing message field.'}, status=400)

        session = ChatSession.objects.filter(user=user, is_active=True).first()
        if not session:
            session = ChatSession.objects.create(
                user=user,
                session_id=uuid.uuid4().hex,
                is_active=True,
            )

        chat_message = ChatMessage.objects.create(
            chat_session=session,
            sender_type='user',
            content=message_text,
        )

        reply_text = f"Received your message: {message_text}. A support agent will respond soon."

        return Response({
            'session_id': session.session_id,
            'message_id': chat_message.id,
            'reply': reply_text,
        }, status=201)
