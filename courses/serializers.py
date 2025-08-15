from rest_framework import serializers
from .models import Course, Category


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

