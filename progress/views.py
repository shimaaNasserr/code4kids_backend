from rest_framework import generics, permissions
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
