from rest_framework import serializers
from .models import Course, Category ,Enrollment, Instructor


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class InstructorSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Instructor
        fields = ['id', 'name', 'bio', 'specialization', 'years_of_experience', 
                 'profile_image', 'email']
        
    def get_profile_image(self, obj):
        try:
            return obj.profile_image.url if obj.profile_image else None
        except Exception:
            return None


class CourseSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True) 
    image_url = serializers.SerializerMethodField()
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
    instructors_names = serializers.CharField(source='get_instructors_names', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'level', 'image_url', 'created_at', 'created_by', 
                 'categories', 'category_ids', 'instructors', 'instructor_ids', 'instructors_names']
        read_only_fields = ['created_by', 'created_at'] 

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  # Nested course data
    kid_name = serializers.CharField(source='kid.username', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'kid_name', 'enrolled_at']