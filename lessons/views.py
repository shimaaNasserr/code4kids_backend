from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from .models import Lesson, LessonCompletion, LessonView
from .serializers import LessonSerializer
import cloudinary.uploader
from accounts.models import User
from courses.models import Course
from django.utils import timezone
from datetime import timedelta

def is_admin(user):
    """Checks if the user is an Admin"""
    return user.is_authenticated and user.role == 'Admin'

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
        if not is_admin(request.user):
            return Response(
                {"error": "Only administrators can create lessons"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = LessonSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
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
        if not is_admin(request.user):
            return Response(
                {"error": "Only administrators can modify lessons"}, 
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
    if not is_admin(request.user):
        return Response(
            {"error": "Only administrators can upload media"}, 
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_lesson_complete(request, lesson_id):
    """تسجيل إكمال درس للطالب - محدث ليشتغل مع نظام التقدم الجديد"""
    if request.user.role != 'Kid':
        return Response(
            {"error": "Only children can mark lessons as complete"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    completion, created = LessonCompletion.objects.get_or_create(
        student=request.user,
        lesson=lesson,
        defaults={'time_spent_minutes': request.data.get('time_spent', 0)}
    )
    
    if not created:
        return Response({
            "message": "Lesson already completed",
            "lesson_id": lesson.id,
            "completed_at": completion.completed_at
        })
    
    return Response({
        "message": f"Lesson completion recorded for: {lesson.title}",
        "lesson_id": lesson.id,
        "completed_at": completion.completed_at
    })

# Admin-specific endpoints
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def admin_lesson_list_create(request):
    """Admin endpoint for listing and creating lessons"""
    if not is_admin(request.user):
        return Response(
            {"error": "Only administrators can access this endpoint"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        lessons = Lesson.objects.all().order_by('course', 'order')
        
        # Filter by course if specified
        course_id = request.query_params.get('course_id')
        if course_id:
            lessons = lessons.filter(course_id=course_id)
            
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LessonSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def admin_lesson_detail(request, pk):
    """Admin endpoint for lesson detail operations"""
    if not is_admin(request.user):
        return Response(
            {"error": "Only administrators can access this endpoint"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    lesson = get_object_or_404(Lesson, pk=pk)
    
    if request.method == 'GET':
        serializer = LessonSerializer(lesson, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_statistics(request):
    if not is_admin(request.user):
        return Response(
            {"error": "Only administrators can access this endpoint"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Calculate statistics
    total_users = User.objects.count()
    total_parents = User.objects.filter(role='Parent').count()
    total_kids = User.objects.filter(role='Kid').count()
    total_courses = Course.objects.count()
    total_lessons = Lesson.objects.count()

    try:
        top_courses = (
            Course.objects.annotate(
                completions_count=Count("lessons__completions", distinct=True),
                views_count=Count("lessons__lessonview", distinct=True),
            )
            .order_by("-completions_count")[:5]
            .values("title", "completions_count", "views_count")
        )
    except Exception as e:
        print("⚠️ Error in top_courses:", e)
        top_courses = []

    # Top Kids (بناءً على completed_lessons related_name)
    try:
        top_kids = (
            User.objects.filter(role="Kid")
            .annotate(completed_lessons_count=Count("completed_lessons", distinct=True))
            .order_by("-completed_lessons_count")[:5]
            .values("username", "completed_lessons_count")
        )
    except Exception as e:
        print("⚠️ Error in top_kids:", e)
        top_kids = []


    statistics = {
        "total_users": total_users,
        "total_parents": total_parents,
        "total_kids": total_kids,
        "total_courses": total_courses,
        "total_lessons": total_lessons,
        "top_courses": list(top_courses),
        "top_kids": list(top_kids),
    }
    
    five_days_ago = timezone.now() - timedelta(days=5)
    active_kids = User.objects.filter(
        role='Kid',
        last_login__gte=five_days_ago
    ).count()

    statistics["active_kids_last_5_days"] = active_kids

    return Response(statistics)
    