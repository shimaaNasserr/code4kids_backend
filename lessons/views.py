from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Lesson
from .serializers import LessonSerializer
import cloudinary.uploader
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.shortcuts import render

def is_admin_or_instructor(user):
    """Checks if the user is an Admin or an Instructor"""
    return user.is_authenticated and user.role in ['Admin', 'Instructor']

@api_view(['GET', 'POST'])
def lesson_list_create(request):
    if request.method == 'GET':
        lessons = Lesson.objects.all().order_by('course', 'order')
        
        course_id = request.query_params.get('course_id')
        if course_id:
            lessons = lessons.filter(course_id=course_id)
            
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not is_admin_or_instructor(request.user):
            return Response(
                {"error": "Only administrators and instructors can create lessons"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = LessonSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            lesson = serializer.save()
            if request.user.role == 'Instructor' and not lesson.instructors.exists():
                lesson.instructors.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    
    if request.method == 'GET':
        serializer = LessonSerializer(lesson, context={'request': request})
        return Response(serializer.data)

    elif request.method in ['PUT', 'DELETE']:
        can_modify = (
            request.user.role == 'Admin' or 
            (request.user.role == 'Instructor' and 
             lesson.instructors.filter(id=request.user.id).exists())
        )
        
        if not can_modify:
            return Response(
                {"error": "You do not have permission to modify this lesson"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        if request.method == 'PUT':
            serializer = LessonSerializer(lesson, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            lesson.delete()
            return Response(
                {"message": "Lesson deleted successfully"}, 
                status=status.HTTP_204_NO_CONTENT
            )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_media(request):
    if not is_admin_or_instructor(request.user):
        return Response(
            {"error": "Only administrators and instructors can upload media"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    file = request.FILES.get('file')
    if not file:
        return Response(
            {"error": "No file was provided"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    resource_type = "video" if file.content_type.startswith("video") else "image"
    
    try:
        upload_result = cloudinary.uploader.upload(
            file,
            resource_type=resource_type,
            folder="lessons"  
        )
        return Response({
            "message": "File uploaded successfully",
            "url": upload_result.get("secure_url"),
            "public_id": upload_result.get("public_id"),
            "resource_type": resource_type
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response(
            {"error": f"Error uploading file: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def mark_lesson_complete(request, lesson_id):
    """Registers lesson completion for a student"""
    if request.user.role != 'Kid':
        return Response(
            {"error": "Only children can mark lessons as complete"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    return Response({
        "message": f"Lesson completion recorded for: {lesson.title}",
        "lesson_id": lesson.id
    })