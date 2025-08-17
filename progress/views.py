from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Progress
from .serializers import ProgressSerializer, DetailedProgressSerializer, ProgressSummarySerializer
from accounts.models import User, KidParentRelation

class ParentProgressListView(generics.ListAPIView):
    serializer_class = DetailedProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Parent':
            return Progress.objects.filter(parent=user).select_related('kid', 'course')
        return Progress.objects.none()


class AdminProgressListView(generics.ListAPIView):
    serializer_class = DetailedProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Progress.objects.all().select_related('kid', 'course', 'parent')
        return Progress.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def kid_progress_detail(request, kid_id):
    user = request.user
    
    if user.role == 'Kid' and user.id != kid_id:
        return Response({"error": "You can only view your own progress"}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    if user.role == 'Parent':
        if not KidParentRelation.objects.filter(parent=user, kid_id=kid_id).exists():
            return Response({"error": "You can only view your children's progress"}, 
                           status=status.HTTP_403_FORBIDDEN)
    
    if user.role not in ['Kid', 'Parent', 'Admin']:
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        kid = User.objects.get(id=kid_id, role='Kid')
    except User.DoesNotExist:
        return Response({"error": "Kid not found"}, status=status.HTTP_404_NOT_FOUND)
    
    progress_list = Progress.objects.filter(kid=kid).select_related('course')
    serializer = DetailedProgressSerializer(progress_list, many=True)
    
    return Response({
        "kid_name": kid.username,
        "kid_id": kid.id,
        "progress": serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def kid_progress_summary(request, kid_id):
    user = request.user
    
    if user.role == 'Kid' and user.id != kid_id:
        return Response({"error": "You can only view your own progress"}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    if user.role == 'Parent':
        if not KidParentRelation.objects.filter(parent=user, kid_id=kid_id).exists():
            return Response({"error": "You can only view your children's progress"}, 
                           status=status.HTTP_403_FORBIDDEN)
    
    if user.role not in ['Kid', 'Parent', 'Admin']:
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        kid = User.objects.get(id=kid_id, role='Kid')
    except User.DoesNotExist:
        return Response({"error": "Kid not found"}, status=status.HTTP_404_NOT_FOUND)
    
    progress_list = Progress.objects.filter(kid=kid)    
    total_courses = progress_list.count()
    completed_courses = progress_list.filter(progress_percentage=100).count()
    in_progress_courses = progress_list.filter(progress_percentage__gt=0, progress_percentage__lt=100).count()
    
    avg_progress = progress_list.aggregate(avg=Avg('progress_percentage'))['avg'] or 0
    total_lessons = sum([p.completed_lessons for p in progress_list])
    total_assignments = sum([p.completed_assignments for p in progress_list])
    
    summary_data = {
        'kid_name': kid.username,
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'in_progress_courses': in_progress_courses,
        'average_progress': round(avg_progress, 2),
        'total_lessons_completed': total_lessons,
        'total_assignments_completed': total_assignments
    }
    
    serializer = ProgressSummarySerializer(summary_data)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def refresh_progress(request, kid_id):
    user = request.user
    
    if user.role not in ['Admin', 'Parent']:
        return Response({"error": "Only Admin or Parent can refresh progress"}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    if user.role == 'Parent':
        if not KidParentRelation.objects.filter(parent=user, kid_id=kid_id).exists():
            return Response({"error": "You can only refresh your children's progress"}, 
                           status=status.HTTP_403_FORBIDDEN)
    
    try:
        kid = User.objects.get(id=kid_id, role='Kid')
    except User.DoesNotExist:
        return Response({"error": "Kid not found"}, status=status.HTTP_404_NOT_FOUND)
    
    progress_list = Progress.objects.filter(kid=kid)
    updated_count = 0
    
    for progress in progress_list:
        progress.update_progress()
        updated_count += 1
    
    return Response({
        "message": f"Progress updated successfully for {kid.username}",
        "updated_records": updated_count
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_performance_note(request, progress_id):
    """إضافة ملاحظة أداء"""
    user = request.user
    
    try:
        progress = Progress.objects.get(id=progress_id)
    except Progress.DoesNotExist:
        return Response({"error": "Progress record not found"}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    if user.role == 'Parent' and progress.parent != user:
        return Response({"error": "You can only add notes to your children's progress"}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    if user.role not in ['Admin', 'Parent']:
        return Response({"error": "Only Admin or Parent can add performance notes"}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    note = request.data.get('note', '').strip()
    if not note:
        return Response({"error": "Note cannot be empty"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    progress.performance_notes = note
    progress.save()
    
    return Response({
        "message": "Performance note added successfully",
        "note": progress.performance_notes
    })