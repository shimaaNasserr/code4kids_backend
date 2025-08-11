from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Lesson
from .serializers import LessonSerializer
from django.views.decorators.csrf import csrf_exempt
import cloudinary.uploader
from django.http import JsonResponse
from django.shortcuts import render

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser | IsAuthenticatedOrReadOnly])
def lesson_list_create(request):
    if request.method == 'GET':
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    
    if request.method == 'GET':
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def upload_media(request):
    file = request.FILES.get('file')
    
    if not file:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Detect if it's video or image
    resource_type = "video" if file.content_type.startswith("video") else "image"
    
    try:
        upload_result = cloudinary.uploader.upload(
            file,
            resource_type=resource_type
        )
        return Response({
            "message": "Upload successful",
            "url": upload_result.get("secure_url"),
            "public_id": upload_result.get("public_id")
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)