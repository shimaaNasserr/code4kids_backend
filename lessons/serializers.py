from rest_framework import serializers
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description','content','is_completed', 'order', 'video_url', 'course', 'created_at']

