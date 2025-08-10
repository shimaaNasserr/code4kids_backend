from rest_framework import serializers
from .models import Progress
from courses.models import Course

class ProgressSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Progress
        fields = ['id', 'parent', 'kid', 'course', 'completed_lessons', 'performance_notes', 'date', 'progress_percentage']

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
            total = course.lessons.count() if hasattr(course, 'lessons') else 0
            if total and value > total:
                raise serializers.ValidationError(f"completed_lessons cannot exceed total lessons ({total}).")
        if value < 0:
            raise serializers.ValidationError("completed_lessons cannot be negative.")
        return value
