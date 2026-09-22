from django.db import models
from django.conf import settings

class ChatSession(models.Model):
    # Total participation: Every chat session must be initiated by a User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_sessions'
    )
    
    # Alternate Key: A unique string identifier (e.g., UUID or unique hash) for session tracking
    session_id = models.CharField(max_length=255, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_human_takeover = models.BooleanField(default=False)
    
    # Partial participation: Can be null until an actual human agent joins the session
    human_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_chats'
    )
    
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Chat Session {self.session_id} - User: {self.user.username}"


class ChatMessage(models.Model):
    # Identifying relationship: A message cannot exist without a ChatSession
    chat_session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    # Sender designation options (User/Customer, AI Bot, or Human Agent)
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'AI Bot'),
    ]
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message by {self.sender_type} at {self.timestamp}"


class ChatMessageAttachment(models.Model):
    """
    Supplemental model resolving the multi-valued 'attachments' attribute on ChatMessage.
    Establishes a Many-to-One relationship back to a single ChatMessage record.
    """
    chat_message = models.ForeignKey(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='chat_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Message ID {self.chat_message.id}"


class HumanSupportSession(models.Model):
    """
    A weak entity capturing dedicated metadata specifically regarding the time periods 
    where a human support workspace workflow takes over the automated chat session.
    """
    # 1:1 total participation: Explicitly maps 1:1 to its parent ChatSession record
    chat_session = models.OneToOneField(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='human_support_details',
        primary_key=True # Implements the weak entity pattern by reusing the parent ID
    )
    
    # Handled by User (Partial participation from both sides as noted in ER diagram)
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='support_sessions'
    )
    
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    resolution_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Human Support Session for Chat {self.chat_session.session_id}"