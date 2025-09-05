from rest_framework import serializers
from .models import CourseRating, LessonRating, InstructorRating
from courses.models import Course, Instructor
from lessons.models import Lesson


class CourseRatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseRating
        fields = [
            'id', 'user', 'user_name', 'course', 'course_title', 
            'rating', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user
        course = data['course']
        
        from courses.models import Enrollment
        if not Enrollment.objects.filter(kid=user, course=course).exists():
            raise serializers.ValidationError(
                "You must be enrolled in this course to rate it."
            )
        
        return data


class LessonRatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    course_title = serializers.CharField(source='lesson.course.title', read_only=True)

    class Meta:
        model = LessonRating
        fields = [
            'id', 'user', 'user_name', 'lesson', 'lesson_title', 
            'course_title', 'rating', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user
        lesson = data['lesson']
        
        from courses.models import Enrollment
        if not Enrollment.objects.filter(kid=user, course=lesson.course).exists():
            raise serializers.ValidationError(
                "You must be enrolled in this lesson's course to rate it."
            )
        
        return data


class InstructorRatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    instructor_name = serializers.CharField(source='instructor.name', read_only=True)

    class Meta:
        model = InstructorRating
        fields = [
            'id', 'user', 'user_name', 'instructor', 'instructor_name',
            'rating', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class CourseRatingStatsSerializer(serializers.Serializer):
    average_rating = serializers.FloatField()
    total_ratings = serializers.IntegerField()
    rating_distribution = serializers.DictField()


class LessonRatingStatsSerializer(serializers.Serializer):
    average_rating = serializers.FloatField()
    total_ratings = serializers.IntegerField()
    rating_distribution = serializers.DictField()


class InstructorRatingStatsSerializer(serializers.Serializer):
    average_rating = serializers.FloatField()
    total_ratings = serializers.IntegerField()
    rating_distribution = serializers.DictField()