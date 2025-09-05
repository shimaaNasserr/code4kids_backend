from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Assignment, Submission
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import AssignmentSerializer, SubmissionSerializer
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from rest_framework.views import APIView

class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'
    
class AssignmentsByLessonListAPIView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Assignment]:  # type: ignore[override]
        lesson_id = self.kwargs.get("lesson_id")
        return Assignment.objects.filter(lesson_id=lesson_id)

class SubmissionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class SubmissionGradeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]

    def patch(self, request, submission_id):
        submission = get_object_or_404(Submission, id=submission_id)
        grade = request.data.get("grade", None)
        feedback = request.data.get("feedback", None)

        if grade is None:
            return Response({"detail": "grade is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            submission.grade = grade
            if feedback is not None:
                submission.feedback = feedback
            submission.save()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Submission graded.", "grade": submission.grade, "feedback": submission.feedback})
