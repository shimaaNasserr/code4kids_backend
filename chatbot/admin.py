from django.contrib import admin
from .models import ChatSession, ChatMessage

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'last_intent', 'created_at', 'updated_at')
    search_fields = ('owner__email', 'last_intent')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender', 'text', 'created_at')
    search_fields = ('text', 'sender')
