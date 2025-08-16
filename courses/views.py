from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Category, Enrollment, Instructor 
from .serializers import CourseSerializer, CategorySerializer, EnrollmentSerializer, InstructorSerializer
from django.shortcuts import get_object_or_404
from accounts.models import User


def is_admin(user):
    return user.is_authenticated and getattr(user, 'role', '') == 'Admin'

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def course_list_create(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        if not is_admin(request.user):
            return Response({'detail': 'Only Admins can create courses.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'GET':
        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not is_admin(request.user):
            return Response({'detail': 'Only Admins can update courses.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not is_admin(request.user):
            return Response({'detail': 'Only Admins can delete courses.'},
                            status=status.HTTP_403_FORBIDDEN)

        course.delete()
        return Response({'detail': 'Course deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def instructor_list_create(request):
    if request.method == 'GET':
        instructors = Instructor.objects.all()
        serializer = InstructorSerializer(instructors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not is_admin(request.user):
            return Response({'detail': 'Only Admins can create instructors.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = InstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def instructor_detail(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)

    if request.method == 'GET':
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not is_admin(request.user):
            return Response({'detail': 'Only Admins can update instructors.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = InstructorSerializer(instructor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not is_admin(request.user):
            return Response({'detail': 'Only Admins can delete instructors.'},
                            status=status.HTTP_403_FORBIDDEN)

        instructor.delete()
        return Response({'detail': 'Instructor deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def category_courses(request, pk):
    category = get_object_or_404(Category, pk=pk)
    courses = category.courses.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_in_course(request):
    course_id = request.data.get('course_id')
    kid_id = request.data.get('kid_id')

    if not course_id:
        return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    course = get_object_or_404(Course, id=course_id)

    if request.user.role == 'Kid':
        kid = request.user
    elif request.user.role in ['Parent', 'Admin']:
        if not kid_id:
            return Response({"error": "kid_id is required for Parent/Admin"}, status=status.HTTP_400_BAD_REQUEST)
        kid = get_object_or_404(User, id=kid_id, role='Kid')
    else:
        return Response({"error": "Invalid role"}, status=status.HTTP_403_FORBIDDEN)

    if Enrollment.objects.filter(kid=kid, course=course).exists():
        return Response({"error": "Kid is already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

    Enrollment.objects.create(kid=kid, course=course)
    return Response({"message": f"{kid.username} enrolled in {course.title} successfully!"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_enrollments(request):
    if request.user.role == 'Kid':
        enrollments = Enrollment.objects.filter(kid=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    elif request.user.role == 'Parent':
        kids = request.user.children_relations.select_related('kid')
        result = []

        for relation in kids:
            kid = relation.kid
            enrollments = Enrollment.objects.filter(kid=kid)
            serializer = EnrollmentSerializer(enrollments, many=True)
            result.append({
                "kid_id": kid.id,
                "kid_name": kid.username,
                "courses": serializer.data
            })

        return Response(result)
    else:
        return Response({"error": "Only Kids or Parents can view enrollments"}, status=403)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unenroll_from_course(request):
    course_id = request.data.get('course_id')
    kid_id = request.data.get('kid_id')

    if not course_id:
        return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    course = get_object_or_404(Course, id=course_id)

    if request.user.role == 'Kid':
        kid = request.user
    elif request.user.role in ['Parent', 'Admin']:
        if not kid_id:
            return Response({"error": "kid_id is required for Parent/Admin"}, status=status.HTTP_400_BAD_REQUEST)
        kid = get_object_or_404(User, id=kid_id, role='Kid')
    else:
        return Response({"error": "Invalid role"}, status=status.HTTP_403_FORBIDDEN)

    enrollment = Enrollment.objects.filter(kid=kid, course=course).first()
    if not enrollment:
        return Response({"error": "Kid is not enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

    enrollment.delete()
    return Response({"message": f"{kid.username} unenrolled from {course.title} successfully!"}, status=status.HTTP_200_OK)