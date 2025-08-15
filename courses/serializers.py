from rest_framework import serializers
from .models import Course, Category ,Enrollment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']



class CourseSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True) 
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'level','image', 'created_at', 'created_by', 'categories']
        read_only_fields = ['created_by', 'created_at'] 

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  # Nesed course data
    kid_name = serializers.CharField(source='kid.username', read_only=True)


    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'kid_name' ,'enrolled_at']