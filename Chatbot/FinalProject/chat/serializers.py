from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ChatMessage, ChatMessageAttachment, ChatSession, HumanSupportSession

User = get_user_model()


class ChatMessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessageAttachment
        fields = ['id', 'chat_message', 'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class ChatMessageSerializer(serializers.ModelSerializer):
    attachments = ChatMessageAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat_session', 'sender_type', 'content', 'timestamp', 'is_read', 'attachments']
        read_only_fields = ['timestamp']


class HumanSupportSessionSerializer(serializers.ModelSerializer):
    agent = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)

    class Meta:
        model = HumanSupportSession
        fields = ['chat_session', 'agent', 'started_at', 'ended_at', 'resolution_notes']
        read_only_fields = ['started_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    human_agent = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    messages = ChatMessageSerializer(many=True, read_only=True)
    human_support_details = HumanSupportSessionSerializer(read_only=True)

    class Meta:
        model = ChatSession
        fields = [
            'id',
            'user',
            'session_id',
            'is_active',
            'is_human_takeover',
            'human_agent',
            'started_at',
            'ended_at',
            'messages',
            'human_support_details',
        ]
        read_only_fields = ['started_at']
