from rest_framework import serializers
from .models import Progress
from courses.models import Course

class ProgressSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    lessons_progress_percentage = serializers.ReadOnlyField()
    assignments_progress_percentage = serializers.ReadOnlyField()
    
    total_lessons_count = serializers.ReadOnlyField()
    total_assignments_count = serializers.ReadOnlyField()
    completed_assignments_count = serializers.ReadOnlyField()
    total_course_items = serializers.ReadOnlyField()
    completed_course_items = serializers.ReadOnlyField()
    
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_level = serializers.CharField(source='course.level', read_only=True)

    class Meta:
        model = Progress
        fields = [
            'id', 'parent', 'kid', 'course', 'course_title', 'course_level',
            'completed_lessons', 'performance_notes', 'date',
            'progress_percentage', 'lessons_progress_percentage', 'assignments_progress_percentage',
            'total_lessons_count', 'total_assignments_count', 'completed_assignments_count',
            'total_course_items', 'completed_course_items'
        ]

    def validate_completed_lessons(self, value):
        course = None
        if 'course' in self.initial_data:
            try:
                course = Course.objects.get(pk=self.initial_data['course'])
            except Course.DoesNotExist:
                raise serializers.ValidationError("Course does not exist.")
        elif getattr(self.instance, 'course', None):
            course = self.instance.course

        if course:
            total_lessons = course.lessons.count()
            if total_lessons and value > total_lessons:
                raise serializers.ValidationError(
                    f"completed_lessons cannot exceed total lessons ({total_lessons})."
                )
        
        if value < 0:
            raise serializers.ValidationError("completed_lessons cannot be negative.")
        return value
