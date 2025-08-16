from rest_framework import serializers
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_instructors = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 
            'title', 
            'description',
            'content',
            'is_completed', 
            'order', 
            'video_url', 
            'course', 
            'course_title',
            'course_instructors',
            'created_at'
        ]
        read_only_fields = ['created_at']

    def get_course_instructors(self, obj):
        return obj.course.get_instructors_names() if obj.course else ""

    def validate_order(self, value):
        course = self.initial_data.get('course')
        if course:
            existing_lesson = Lesson.objects.filter(course=course, order=value)
            if self.instance:
                existing_lesson = existing_lesson.exclude(id=self.instance.id)
            if existing_lesson.exists():
                raise serializers.ValidationError(
                    f"A lesson with the order {value} already exists in this course."
                )
        return value