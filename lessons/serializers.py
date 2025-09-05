from rest_framework import serializers
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_instructors = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()  
    duration_minutes = serializers.IntegerField(read_only=True)

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
            'duration_minutes',
            'is_published',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_is_completed(self, obj):
        """Check if the current user has completed this lesson"""
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return obj.is_completed_by_user(request.user)
        return False

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