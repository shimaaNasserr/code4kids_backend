from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, UserProfile, KidParentRelation
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserProfileSerializer
from courses.models import Enrollment, Course
from progress.models import Progress
from lessons.models import LessonCompletion
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
from rest_framework import status
import re


@api_view(['POST'])
def register(request):
    data = request.data

    required_fields = ['username', 'email', 'password', 'confirm_password', 'role']
    for field in required_fields:
        if field not in data or not data[field].strip():
            return Response({"error": f"{field} is required."}, status=400)

    if data['role'].lower() == 'admin':
        return Response({"error": "You are not allowed to register as an Admin."}, status=403)
        
    if data['password'] != data['confirm_password']:
        return Response({"error": "Passwords do not match."}, status=400)

    if data['role'] not in ['Kid', 'Parent']:
        return Response({"error": "Role must be either 'Kid' or 'Parent'."}, status=400)

    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()

        if user.role == 'Admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()

        return Response({ 
            "message": "User Registered", 
            "user": UserSerializer(user).data 
        }, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def loginUser(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            },
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, status=200)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def parent_only_view(request):
    if request.user.role != 'Parent':
        return Response({"error": "Access denied. Parent role required."}, status=403)

    return Response({"message": f"Hello {request.user.first_name}, welcome to the Parent Dashboard!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kid_only_view(request):
    if request.user.role != 'Kid':
        return Response({"error": "Access denied. Kid role required."}, status=403)

    return Response({"message": f"Hello {request.user.first_name}, welcome to the Kid Zone!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_only_view(request):
    if request.user.role != 'Admin':
        return Response({"error": "Access denied. Admin role required."}, status=403)

    return Response({"message": f"Welcome Admin {request.user.first_name} to the Admin Panel!"})


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_full_user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    profile = user.profile
    
    user_data = {
        'first_name': request.data.get('first_name', user.first_name),
        'last_name': request.data.get('last_name', user.last_name),
        'phone_number': request.data.get('phone_number', user.phone_number),
    }
    
    for key, value in user_data.items():
        setattr(user, key, value)
    user.save()
    
    profile_serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if profile_serializer.is_valid():
        profile_serializer.save()
        
        user_serializer = UserSerializer(user)
        return Response({
            "message": "Profile updated successfully",
            "user": user_serializer.data
        })
    
    return Response(profile_serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_points(request):
    user = request.user
    points = request.data.get('points', 0)
    
    if points > 0:
        user.profile.points += points
        user.profile.save()
        
        return Response({
            "message": f"Added {points} points",
            "total_points": user.profile.points
        })
    
    return Response({"error": "Invalid points value"}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_dashboard(request):
  
    user = request.user
    
    profile_data = {
        'user_info': {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role,
        },
        'profile_info': {
            'avatar': user.profile.avatar.url if user.profile.avatar else None,
            'bio': user.profile.bio,
            'age': user.profile.age,
            'favorite_language': user.profile.favorite_language,
            'skill_level': user.profile.skill_level,
            'points': user.profile.points,
            'courses_completed': user.profile.courses_completed,
            'badges': user.profile.badges,
        }
    }
    
    if user.role == 'Kid':
        enrollments = Enrollment.objects.filter(kid=user, is_active=True)
        total_courses = enrollments.count()
        
        progress_entries = Progress.objects.filter(kid=user)
        avg_progress = progress_entries.aggregate(
            avg_progress=Avg('completed_lessons')
        )['avg_progress'] or 0
        
        total_completed_lessons = LessonCompletion.objects.filter(
            student=user
        ).count()
        
        profile_data['learning_stats'] = {
            'total_enrolled_courses': total_courses,
            'total_completed_lessons': total_completed_lessons,
            'average_progress': round(avg_progress, 2),
            'current_courses': []
        }
        
        for enrollment in enrollments:
            try:
                progress = Progress.objects.get(kid=user, course=enrollment.course)
                course_progress = progress.progress_percentage()
            except Progress.DoesNotExist:
                course_progress = 0
                
            profile_data['learning_stats']['current_courses'].append({
                'course_id': enrollment.course.id,
                'course_title': enrollment.course.title,
                'course_image': enrollment.course.image.url if enrollment.course.image else None,
                'progress_percentage': course_progress,
                'enrolled_at': enrollment.enrolled_at,
                'total_lessons': enrollment.course.total_lessons,
                'completed_lessons': progress.completed_lessons if 'progress' in locals() else 0,
            })
    
    elif user.role == 'Parent':
        children = KidParentRelation.objects.filter(parent=user)
        
        profile_data['children'] = []
        for relation in children:
            kid = relation.kid
            kid_enrollments = Enrollment.objects.filter(kid=kid, is_active=True).count()
            kid_completed = LessonCompletion.objects.filter(student=kid).count()
            
            profile_data['children'].append({
                'kid_id': kid.id,
                'kid_name': f"{kid.first_name} {kid.last_name}",
                'kid_username': kid.username,
                'total_courses': kid_enrollments,
                'total_completed_lessons': kid_completed,
                'kid_points': kid.profile.points,
            })
    
    return Response(profile_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
   
    if 'avatar' not in request.FILES:
        return Response({
            'error': 'No avatar file provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    profile = user.profile
    
    if profile.avatar:
        profile.avatar.delete()
    
    profile.avatar = request.FILES['avatar']
    profile.save()
    
    return Response({
        'message': 'Avatar uploaded successfully',
        'avatar_url': profile.avatar.url
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_progress_detail(request, course_id):
   
    user = request.user
    
    enrollment = get_object_or_404(
        Enrollment, 
        kid=user, 
        course_id=course_id, 
        is_active=True
    )
    
    course = enrollment.course
    
    try:
        progress = Progress.objects.get(kid=user, course=course)
    except Progress.DoesNotExist:
        progress = None
    
    completed_lessons = LessonCompletion.objects.filter(
        student=user,
        lesson__course=course
    ).values_list('lesson_id', flat=True)
    
    course_data = {
        'course_id': course.id,
        'course_title': course.title,
        'course_description': course.description,
        'course_level': course.level,
        'total_lessons': course.total_lessons,
        'total_assignments': course.total_assignments,
        'completed_lessons': progress.completed_lessons if progress else 0,
        'completed_assignments': progress.completed_assignments if progress else 0,
        'progress_percentage': progress.progress_percentage() if progress else 0,
        'enrolled_at': enrollment.enrolled_at,
        'completed_lesson_ids': list(completed_lessons),
    }
    
    return Response(course_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def achievements(request):
   
    user = request.user
    profile = user.profile
    
    achievements_data = {
        'total_points': profile.points,
        'courses_completed': profile.courses_completed,
        'badges': profile.badges,
        'current_streak': 0, 
        'achievements': []
    }
    
    total_lessons = LessonCompletion.objects.filter(student=user).count()
    
    if total_lessons >= 1:
        achievements_data['achievements'].append({
            'title': 'First Steps',
            'description': 'أكمل أول درس',
            'icon': '🎯',
            'unlocked': True
        })
    
    if total_lessons >= 10:
        achievements_data['achievements'].append({
            'title': 'Getting Started',
            'description': 'أكمل 10 دروس',
            'icon': '⭐',
            'unlocked': True
        })
    
    if profile.courses_completed >= 1:
        achievements_data['achievements'].append({
            'title': 'Course Master',
            'description': 'أكمل أول كورس',
            'icon': '🏆',
            'unlocked': True
        })
    
    return Response(achievements_data, status=status.HTTP_200_OK)