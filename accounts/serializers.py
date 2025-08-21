# accounts/serializers.py
from rest_framework import serializers
from .models import User, UserProfile, KidParentRelation
from courses.models import Enrollment, Course
from progress.models import Progress
from lessons.models import LessonCompletion
from django.contrib.auth import get_user_model
import re




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        pattern = r'^[A-Za-z0-9@#$%^&*]{6,11}$'
        if not re.match(pattern, data['password']):
            raise serializers.ValidationError(
                {"password": "Password must be 6–11 characters long, and may include @#$%^&* only."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        data['user'] = user
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    avatar = serializers.ImageField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'birth_date', 'favorite_language', 
            'skill_level', 'points', 'courses_completed', 
            'badges', 'age', 'created_at', 'updated_at'
        ]

# class UserBasicInfoSerializer(serializers.ModelSerializer):
#    
#     profile = UserProfileSerializer(read_only=True)
    
#     class Meta:
#         model = User
#         fields = [
#             'id', 'username', 'email', 'first_name', 'last_name', 
#             'role', 'phone_number', 'profile'
#         ]
#         extra_kwargs = {
#             'email': {'read_only': True}
#         }


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone_number', 'profile'
        ]
        extra_kwargs = {
            'email': {'read_only': True}
        }

class ProfileUpdateSerializer(serializers.Serializer):
    
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    bio = serializers.CharField(max_length=300, required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    favorite_language = serializers.ChoiceField(
        choices=[
            ('Python', 'Python'),
            ('JavaScript', 'JavaScript'),
            ('Scratch', 'Scratch'),
            ('HTML/CSS', 'HTML/CSS'),
        ],
        required=False,
        allow_blank=True
    )
    skill_level = serializers.ChoiceField(
        choices=[
            ('Beginner'),
            ('Intermediate'),
            ('Advanced')
        ],
        required=False
    )

class CourseProgressSerializer(serializers.ModelSerializer):
   
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_image = serializers.ImageField(source='course.image', read_only=True)
    course_level = serializers.CharField(source='course.level', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Progress
        fields = [
            'course', 'course_title', 'course_image', 'course_level',
            'completed_lessons', 'completed_assignments', 
            'progress_percentage', 'last_updated'
        ]
    
    def get_progress_percentage(self, obj):
        return obj.progress_percentage()

class EnrollmentSummarySerializer(serializers.ModelSerializer):
    
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_image = serializers.ImageField(source='course.image', read_only=True)
    course_level = serializers.CharField(source='course.level', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    completed_lessons = serializers.SerializerMethodField()
    
    class Meta:
        model = Enrollment
        fields = [
            'course', 'course_title', 'course_image', 'course_level',
            'enrolled_at', 'completion_percentage', 'progress_percentage',
            'completed_lessons'
        ]
    
    def get_progress_percentage(self, obj):
        try:
            progress = Progress.objects.get(kid=obj.kid, course=obj.course)
            return progress.progress_percentage()
        except Progress.DoesNotExist:
            return 0
    
    def get_completed_lessons(self, obj):
        return LessonCompletion.objects.filter(
            student=obj.kid,
            lesson__course=obj.course
        ).count()

class KidSummarySerializer(serializers.ModelSerializer):
    
    kid_name = serializers.SerializerMethodField()
    total_courses = serializers.SerializerMethodField()
    total_completed_lessons = serializers.SerializerMethodField()
    kid_points = serializers.SerializerMethodField()
    kid_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = KidParentRelation
        fields = [
            'kid', 'kid_name', 'total_courses', 
            'total_completed_lessons', 'kid_points', 'kid_avatar'
        ]
    
    def get_kid_name(self, obj):
        return f"{obj.kid.first_name} {obj.kid.last_name}".strip() or obj.kid.username
    
    def get_total_courses(self, obj):
        return Enrollment.objects.filter(kid=obj.kid, is_active=True).count()
    
    def get_total_completed_lessons(self, obj):
        return LessonCompletion.objects.filter(student=obj.kid).count()
    
    def get_kid_points(self, obj):
        return obj.kid.profile.points
    
    def get_kid_avatar(self, obj):
        if obj.kid.profile.avatar:
            return obj.kid.profile.avatar.url
        return None

class AchievementSerializer(serializers.Serializer):
    
    title = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField()
    unlocked = serializers.BooleanField()
    unlocked_at = serializers.DateTimeField(required=False, allow_null=True)

class LessonCompletionStatsSerializer(serializers.ModelSerializer):
   
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    course_title = serializers.CharField(source='lesson.course.title', read_only=True)
    
    class Meta:
        model = LessonCompletion
        fields = [
            'lesson', 'lesson_title', 'course_title',
            'completed_at', 'time_spent_minutes', 'notes'
        ]

class ComprehensiveProfileSerializer(serializers.ModelSerializer):
   
    profile = UserProfileSerializer(read_only=True)
    enrolled_courses = serializers.SerializerMethodField()
    recent_completions = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone_number', 'profile', 'enrolled_courses',
            'recent_completions', 'children'
        ]
    
    def get_enrolled_courses(self, obj):
        if obj.role == 'Kid':
            enrollments = Enrollment.objects.filter(kid=obj, is_active=True)
            return EnrollmentSummarySerializer(enrollments, many=True).data
        return []
    
    def get_recent_completions(self, obj):
        if obj.role == 'Kid':
            completions = LessonCompletion.objects.filter(student=obj).order_by('-completed_at')[:5]
            return LessonCompletionStatsSerializer(completions, many=True).data
        return []
    
    def get_children(self, obj):
        if obj.role == 'Parent':
            relations = KidParentRelation.objects.filter(parent=obj)
            return KidSummarySerializer(relations, many=True).data
        return []