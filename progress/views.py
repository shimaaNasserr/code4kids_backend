from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Progress
from .serializers import ProgressSerializer


# -------------------- CHILD DASHBOARD --------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def child_dashboard(request):
    user = request.user
    if user.role != "Kid":
        return Response({"error": "Only kids can access this endpoint"}, status=403)

    progresses = Progress.objects.filter(kid=user).select_related("course")
    serializer = ProgressSerializer(progresses, many=True)

    return Response({
        "child": user.username,
        "progress": serializer.data
    })


# -------------------- PARENT DASHBOARD --------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def parent_dashboard(request):
    user = request.user
    if user.role != "Parent":
        return Response({"error": "Only parents can access this endpoint"}, status=403)

    children_data = []
    children = user.children.all()

    for child in children:
        child_progresses = Progress.objects.filter(kid=child).select_related("course")
        serializer = ProgressSerializer(child_progresses, many=True)

        children_data.append({
            "child": child.username,
            "progress": serializer.data
        })

    return Response({
        "parent": user.username,
        "children_progress": children_data
    })
