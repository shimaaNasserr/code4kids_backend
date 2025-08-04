from rest_framework import serializers
from .models import Course, Lesson, Assignment

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
