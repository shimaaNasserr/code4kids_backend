from rest_framework import serializers
from .models import Progress
from courses.models import Course

class ProgressSerializer(serializers.ModelSerializer):
    total_lessons = serializers.SerializerMethodField()
    total_assignments = serializers.SerializerMethodField()
    completed_lessons = serializers.SerializerMethodField()
    completed_assignments = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    course_title = serializers.CharField(source='course.title', read_only=True)
    kid_name = serializers.CharField(source='kid.username', read_only=True)
    parent_name = serializers.CharField(source='parent.username', read_only=True)

    class Meta:
        model = Progress
        fields = [
            "id", "kid_name","parent_name", "course_title",
            "total_lessons", "completed_lessons",
            "total_assignments", "completed_assignments",
            "progress_percentage",
        ]

    def get_total_lessons(self, obj):
        return obj.total_lessons()

    def get_total_assignments(self, obj):
        return obj.total_assignments()

    def get_completed_lessons(self, obj):
        return obj.completed_lessons_count()

    def get_completed_assignments(self, obj):
        return obj.completed_assignments_count()

    def get_progress_percentage(self, obj):
        return obj.progress_percentage()