from rest_framework import serializers
from .models import Course, Category ,Enrollment, Instructor


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'name', 'bio', 'specialization', 'years_of_experience', 
                 'profile_image', 'email']


class CourseSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True) 
    instructors = InstructorSerializer(many=True, read_only=True)
    instructor_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        write_only=True, 
        queryset=Instructor.objects.all(),
        source='instructors',
        required=False
    )
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Category.objects.all(),
        source='categories',
        required=False
    )
    image = serializers.ImageField(use_url=True, required=False)
    instructors_names = serializers.CharField(source='get_instructors_names', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'level', 'image', 'created_at', 'created_by', 
                 'categories', 'category_ids', 'instructors', 'instructor_ids', 'instructors_names']
        read_only_fields = ['created_by', 'created_at'] 


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  # Nested course data
    kid_name = serializers.CharField(source='kid.username', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'kid_name', 'enrolled_at']