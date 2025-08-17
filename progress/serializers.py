from rest_framework import serializers
from .models import Progress
from courses.models import Course

class ProgressSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    lessons_progress_percentage = serializers.ReadOnlyField()
    assignments_progress_percentage = serializers.ReadOnlyField()
    total_lessons = serializers.ReadOnlyField()
    total_assignments = serializers.ReadOnlyField()
    total_activities = serializers.ReadOnlyField()
    completed_activities = serializers.ReadOnlyField()
    course_title = serializers.CharField(source='course.title', read_only=True)
    kid_name = serializers.CharField(source='kid.username', read_only=True)
    parent_name = serializers.CharField(source='parent.username', read_only=True)

    class Meta:
        model = Progress
        fields = [
            'id', 'parent', 'kid', 'course', 'course_title', 'kid_name', 'parent_name',
            'completed_lessons', 'completed_assignments', 'performance_notes', 
            'date', 'last_updated',
            'total_lessons', 'total_assignments', 'total_activities', 
            'completed_activities', 'progress_percentage',
            'lessons_progress_percentage', 'assignments_progress_percentage'
        ]
        read_only_fields = [
            'date', 'last_updated', 'total_lessons', 'total_assignments',
            'total_activities', 'completed_activities', 'progress_percentage',
            'lessons_progress_percentage', 'assignments_progress_percentage'
        ]

    def validate_completed_lessons(self, value):
        if value < 0:
            raise serializers.ValidationError("completed_lessons cannot be negative.")
        return value

    def validate_completed_assignments(self, value):
        if value < 0:
            raise serializers.ValidationError("completed_assignments cannot be negative.")
        return value


class DetailedProgressSerializer(ProgressSerializer):
    actual_progress = serializers.SerializerMethodField()
    
    class Meta(ProgressSerializer.Meta):
        fields = ProgressSerializer.Meta.fields + ['actual_progress']
    
    def get_actual_progress(self, obj):
        return obj.calculate_actual_progress()


class ProgressSummarySerializer(serializers.Serializer):
    kid_name = serializers.CharField()
    total_courses = serializers.IntegerField()
    completed_courses = serializers.IntegerField()
    in_progress_courses = serializers.IntegerField()
    average_progress = serializers.FloatField()
    total_lessons_completed = serializers.IntegerField()
    total_assignments_completed = serializers.IntegerField()