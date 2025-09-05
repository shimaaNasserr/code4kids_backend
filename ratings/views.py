from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q
from .models import CourseRating, LessonRating, InstructorRating
from .serializers import (
    CourseRatingSerializer, LessonRatingSerializer, InstructorRatingSerializer,
    CourseRatingStatsSerializer, LessonRatingStatsSerializer, InstructorRatingStatsSerializer
)
from courses.models import Course, Instructor
from lessons.models import Lesson


def is_kid(user):
    """Check if user is a Kid"""
    return user.is_authenticated and user.role == 'Kid'


# ========== Course Rating Views ==========

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def course_rating_list_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'GET':
        ratings = CourseRating.objects.filter(course=course)
        serializer = CourseRatingSerializer(ratings, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not is_kid(request.user):
            return Response(
                {"error": "Only kids can rate courses"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data.copy()
        data['course'] = course.id
        
        serializer = CourseRatingSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def course_rating_detail(request, course_id, rating_id):
    course = get_object_or_404(Course, id=course_id)
    rating = get_object_or_404(CourseRating, id=rating_id, course=course)
    
    # Only the owner can modify their rating
    if rating.user != request.user and request.user.role != 'Admin':
        return Response(
            {"error": "You can only modify your own ratings"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        serializer = CourseRatingSerializer(rating)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CourseRatingSerializer(rating, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        rating.delete()
        return Response({"message": "Rating deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def course_rating_stats(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    ratings = CourseRating.objects.filter(course=course)
    total_ratings = ratings.count()
    
    if total_ratings == 0:
        return Response({
            "average_rating": 0,
            "total_ratings": 0,
            "rating_distribution": {str(i): 0 for i in range(1, 6)}
        })
    
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    
    # حساب توزيع التقييمات
    rating_distribution = {}
    for i in range(1, 6):
        count = ratings.filter(rating=i).count()
        rating_distribution[str(i)] = count
    
    stats = {
        "average_rating": round(average_rating, 2),
        "total_ratings": total_ratings,
        "rating_distribution": rating_distribution
    }
    
    serializer = CourseRatingStatsSerializer(stats)
    return Response(serializer.data)


# ========== Lesson Rating Views ==========

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lesson_rating_list_create(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if request.method == 'GET':
        ratings = LessonRating.objects.filter(lesson=lesson)
        serializer = LessonRatingSerializer(ratings, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not is_kid(request.user):
            return Response(
                {"error": "Only kids can rate lessons"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data.copy()
        data['lesson'] = lesson.id
        
        serializer = LessonRatingSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def lesson_rating_detail(request, lesson_id, rating_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    rating = get_object_or_404(LessonRating, id=rating_id, lesson=lesson)
    
    # Only the owner can modify their rating
    if rating.user != request.user and request.user.role != 'Admin':
        return Response(
            {"error": "You can only modify your own ratings"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        serializer = LessonRatingSerializer(rating)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = LessonRatingSerializer(rating, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        rating.delete()
        return Response({"message": "Rating deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def lesson_rating_stats(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    ratings = LessonRating.objects.filter(lesson=lesson)
    total_ratings = ratings.count()
    
    if total_ratings == 0:
        return Response({
            "average_rating": 0,
            "total_ratings": 0,
            "rating_distribution": {str(i): 0 for i in range(1, 6)}
        })
    
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    
    rating_distribution = {}
    for i in range(1, 6):
        count = ratings.filter(rating=i).count()
        rating_distribution[str(i)] = count
    
    stats = {
        "average_rating": round(average_rating, 2),
        "total_ratings": total_ratings,
        "rating_distribution": rating_distribution
    }
    
    serializer = LessonRatingStatsSerializer(stats)
    return Response(serializer.data)


# ========== Instructor Rating Views ==========

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def instructor_rating_list_create(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    
    if request.method == 'GET':
        ratings = InstructorRating.objects.filter(instructor=instructor)
        serializer = InstructorRatingSerializer(ratings, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not is_kid(request.user):
            return Response(
                {"error": "Only kids can rate instructors"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data.copy()
        data['instructor'] = instructor.id
        
        serializer = InstructorRatingSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def instructor_rating_detail(request, instructor_id, rating_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    rating = get_object_or_404(InstructorRating, id=rating_id, instructor=instructor)
    
    # Only the owner can modify their rating
    if rating.user != request.user and request.user.role != 'Admin':
        return Response(
            {"error": "You can only modify your own ratings"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        serializer = InstructorRatingSerializer(rating)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = InstructorRatingSerializer(rating, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        rating.delete()
        return Response({"message": "Rating deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def instructor_rating_stats(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    
    ratings = InstructorRating.objects.filter(instructor=instructor)
    total_ratings = ratings.count()
    
    if total_ratings == 0:
        return Response({
            "average_rating": 0,
            "total_ratings": 0,
            "rating_distribution": {str(i): 0 for i in range(1, 6)}
        })
    
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    
    rating_distribution = {}
    for i in range(1, 6):
        count = ratings.filter(rating=i).count()
        rating_distribution[str(i)] = count
    
    stats = {
        "average_rating": round(average_rating, 2),
        "total_ratings": total_ratings,
        "rating_distribution": rating_distribution
    }
    
    serializer = InstructorRatingStatsSerializer(stats)
    return Response(serializer.data)


# ========== User's Own Ratings ==========

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_ratings(request):
    """Get all ratings by the authenticated user"""
    if not is_kid(request.user):
        return Response(
            {"error": "Only kids can view their ratings"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    course_ratings = CourseRating.objects.filter(user=request.user)
    lesson_ratings = LessonRating.objects.filter(user=request.user)
    instructor_ratings = InstructorRating.objects.filter(user=request.user)
    
    return Response({
        "course_ratings": CourseRatingSerializer(course_ratings, many=True).data,
        "lesson_ratings": LessonRatingSerializer(lesson_ratings, many=True).data,
        "instructor_ratings": InstructorRatingSerializer(instructor_ratings, many=True).data
    })