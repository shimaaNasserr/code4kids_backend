# progress/serializers.py
from rest_framework import serializers
from .models import Progress
from courses.models import Course


class CourseMiniSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "level", "image_url"]

    def get_image_url(self, obj):
        if obj.image:
            try:
                return obj.image.url  # CloudinaryField بيرجع URL مباشر كده
            except:
                return None
        return None


class ProgressSerializer(serializers.ModelSerializer):
    total_lessons = serializers.SerializerMethodField()
    total_assignments = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    course = CourseMiniSerializer(read_only=True)

    class Meta:
        model = Progress
        fields = [
            "id",
            "course",
            "total_lessons",
            "completed_lessons",
            "total_assignments",
            "completed_assignments",
            "progress_percentage",
        ]

    def get_total_lessons(self, obj):
        return obj.total_lessons()

    def get_total_assignments(self, obj):
        return obj.total_assignments()

    def get_progress_percentage(self, obj):
        return obj.progress_percentage()
