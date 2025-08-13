from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Progress
from .serializers import ProgressSerializer

class ParentProgressListView(generics.ListAPIView):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Parent':
            return Progress.objects.filter(parent=user)
        return Progress.objects.none()


class AdminProgressListView(generics.ListAPIView):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Progress.objects.all()
        return Progress.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_kid_progress(request, course_id):
    try:
        if request.user.role == 'Kid':
            progress = Progress.objects.get(kid=request.user, course_id=course_id)
        elif request.user.role == 'Parent':
            kid_id = request.GET.get('kid_id')
            if not kid_id:
                return Response({'error': 'kid_id is required for parents'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            progress = Progress.objects.get(parent=request.user, kid_id=kid_id, course_id=course_id)
        elif request.user.role == 'Admin':
            kid_id = request.GET.get('kid_id')
            if not kid_id:
                return Response({'error': 'kid_id is required for admins'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            progress = Progress.objects.get(kid_id=kid_id, course_id=course_id)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProgressSerializer(progress)
        return Response(serializer.data)
    
    except Progress.DoesNotExist:
        return Response({'error': 'Progress record not found'}, 
                       status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_lesson_progress(request, course_id):
    if request.user.role != 'Kid':
        return Response({'error': 'Only kids can update their lesson progress'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    try:
        progress = Progress.objects.get(kid=request.user, course_id=course_id)
        lessons_completed = request.data.get('completed_lessons')
        
        if lessons_completed is None:
            return Response({'error': 'completed_lessons is required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            lessons_completed = int(lessons_completed)
        except ValueError:
            return Response({'error': 'completed_lessons must be a number'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        new_percentage = progress.update_lesson_progress(lessons_completed)
        
        return Response({
            'message': 'Progress updated successfully',
            'progress_percentage': new_percentage,
            'completed_lessons': progress.completed_lessons,
            'total_lessons': progress.total_lessons_count
        })
    
    except Progress.DoesNotExist:
        return Response({'error': 'Progress record not found'}, 
                       status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_detailed_progress(request, course_id):
    try:
        if request.user.role == 'Kid':
            progress = Progress.objects.get(kid=request.user, course_id=course_id)
        elif request.user.role == 'Parent':
            kid_id = request.GET.get('kid_id')
            if not kid_id:
                return Response({'error': 'kid_id is required for parents'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            progress = Progress.objects.get(parent=request.user, kid_id=kid_id, course_id=course_id)
        elif request.user.role == 'Admin':
            kid_id = request.GET.get('kid_id')
            if not kid_id:
                return Response({'error': 'kid_id is required for admins'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            progress = Progress.objects.get(kid_id=kid_id, course_id=course_id)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        detailed_progress = progress.get_detailed_progress()
        
        return Response({
            'kid': progress.kid.username,
            'course': progress.course.title,
            'progress_details': detailed_progress
        })
    
    except Progress.DoesNotExist:
        return Response({'error': 'Progress record not found'}, 
                       status=status.HTTP_404_NOT_FOUND)