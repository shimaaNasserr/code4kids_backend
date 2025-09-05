from courses.models import Course
from courses.serializers import CourseSerializer

def route_intent(message, user, child=None):
    msg = message.lower()

    if "عدد الكورسات" in msg or "الكورسات المتاحة" in msg or "انا مسجل في ايه" in msg:
        courses = Course.objects.all()
        courses_ser = CourseSerializer(courses, many=True).data

        reply_text = f"دي الكورسات المتاحة حالياً: {len(courses_ser)} كورس."
        reply_data = {"courses": courses_ser}
        intent_name = "list_courses"
        return reply_text, reply_data, intent_name

    # أي رسالة غير مفهومة
    reply_text = "مش فاهم سؤالك 😅، جرّب تسأل بطريقة تانية."
    reply_data = {}
    intent_name = "unknown"
    return reply_text, reply_data, intent_name
