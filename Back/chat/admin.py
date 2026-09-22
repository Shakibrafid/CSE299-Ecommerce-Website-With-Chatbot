from django.contrib import admin

from .models import (
	ChatMessage,
	ChatMessageAttachment,
	ChatSession,
	HumanSupportSession,
)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
	list_display = ['session_id', 'user', 'is_active', 'is_human_takeover', 'started_at', 'ended_at']
	list_filter = ['is_active', 'is_human_takeover', 'started_at']
	search_fields = ['session_id', 'user__username', 'user__email']
	readonly_fields = ['started_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
	list_display = ['chat_session', 'sender_type', 'is_read', 'timestamp']
	list_filter = ['sender_type', 'is_read', 'timestamp']
	search_fields = ['chat_session__session_id', 'content']
	readonly_fields = ['timestamp']


@admin.register(ChatMessageAttachment)
class ChatMessageAttachmentAdmin(admin.ModelAdmin):
	list_display = ['chat_message', 'uploaded_at']
	search_fields = ['chat_message__content']
	readonly_fields = ['uploaded_at']


@admin.register(HumanSupportSession)
class HumanSupportSessionAdmin(admin.ModelAdmin):
	list_display = ['chat_session', 'agent', 'started_at', 'ended_at']
	list_filter = ['started_at', 'ended_at']
	search_fields = ['chat_session__session_id', 'agent__username', 'resolution_notes']
	readonly_fields = ['started_at']
