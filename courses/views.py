from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  
def course_list_create(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user_role = getattr(request.user, 'role', None)
        if user_role not in ['Admin', 'Parent']:
            return Response({'detail': 'Only Admins and Parents can create courses.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user if request.user.is_authenticated else None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    elif request.method == 'PUT':
        user_role = getattr(request.user, 'role', None)
        if (not request.user.is_authenticated) or (course.created_by != request.user and user_role != 'Admin'):
            return Response({'detail': 'Not allowed to update this course.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_role = getattr(request.user, 'role', None)
        if (not request.user.is_authenticated) or (course.created_by != request.user and user_role != 'Admin'):
            return Response({'detail': 'Not allowed to delete this course.'}, status=status.HTTP_403_FORBIDDEN)

        course.delete()
        return Response({'detail': 'Course deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
