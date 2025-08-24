from django.urls import path
from .views import ChatbotView, ChatHistoryView

urlpatterns = [
    path('', ChatbotView.as_view(), name='chatbot'),
    path('history/<uuid:session_id>/', ChatHistoryView.as_view(), name='chat_history'),
]
