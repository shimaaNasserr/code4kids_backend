from rest_framework import serializers
from .models import Lesson
from accounts.serializers import UserSerializer

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSerializer.Meta.model
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'specialization', 
                 'years_of_experience', 'profile_image']

class LessonSerializer(serializers.ModelSerializer):
    instructors = InstructorSerializer(many=True, read_only=True)
    instructor_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        write_only=True, 
        queryset=UserSerializer.Meta.model.objects.filter(role='Instructor'),
        source='instructors'
    )
    course_title = serializers.CharField(source='course.title', read_only=True)
    instructors_names = serializers.CharField(source='get_instructors_names', read_only=True)

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
            'created_at',
            'instructors',
            'instructor_ids',
            'instructors_names'
        ]
        read_only_fields = ['created_at']

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