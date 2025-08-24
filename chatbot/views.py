from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer
from .intents import route_intent
import uuid



class ChatbotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        message = (request.data.get("message") or "").strip()
        session_id = request.data.get("session_id")
        user = request.user if request.user.is_authenticated else None

        if not message:
            return Response({"detail": "message is required"}, status=400)

        session = None
        if session_id:
            try:
                session_uuid = uuid.UUID(session_id)
                if user:
                    session = ChatSession.objects.get(id=session_uuid, owner=user)
                else:
                    session = ChatSession.objects.get(id=session_uuid, owner__isnull=True)
            except (ChatSession.DoesNotExist, ValueError):
                # لو session_id غير صالح أو مش موجود، نخلق session جديد
                session = ChatSession.objects.create(owner=user)
        else:
            session = ChatSession.objects.create(owner=user)

        # خزّن رسالة المستخدم
        ChatMessage.objects.create(session=session, sender='user', text=message)

        # شغّل الراوتر لمعالجة الرسالة
        try:
            reply_text, reply_data, intent_name = route_intent(message, user)
        except Exception as e:
            # لو حصل خطأ في معالجة الرسالة
            reply_text = "حصل خطأ أثناء معالجة رسالتك."
            reply_data = None
            intent_name = None
            print("Error in route_intent:", e)

        # حدّث آخر intent في الـ session
        session.last_intent = intent_name
        session.save()

        # خزّن رد البوت
        bot_msg = ChatMessage.objects.create(
            session=session,
            sender='bot',
            text=reply_text,
            data=reply_data or {}
        )

        return Response({
            "session_id": str(session.id),
            "reply": reply_text,
            "data": reply_data,
            "intent": intent_name,
            "message_id": str(bot_msg.id),
        }, status=200)

class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, owner=request.user)
        except ChatSession.DoesNotExist:
            return Response({"detail": "Session not found"}, status=404)

        ser = ChatSessionSerializer(session)
        return Response(ser.data, status=200)
