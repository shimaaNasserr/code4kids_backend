from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Progress
from accounts.models import KidParentRelation
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
    parent = request.user

    # علاقات الأب والأطفال
    relations = KidParentRelation.objects.filter(parent=parent).select_related("kid")

    children_data = []

    for relation in relations:
        kid = relation.kid
        progresses = Progress.objects.filter(kid=kid).select_related("course")

        total_courses = progresses.count()
        in_progress = 0
        completed = 0

        for p in progresses:
            p.recompute(save=False)
            pct = p.progress_percentage()
            if pct >= 100:
                completed += 1
            elif pct > 0:
                in_progress += 1

        children_data.append({
            "id": kid.id,
            "name": f"{kid.first_name} {kid.last_name}".strip() or kid.username,
            "avatar": kid.profile.avatar.url if kid.profile and kid.profile.avatar else None,
            "stats": {
                "total_courses": total_courses,
                "in_progress": in_progress,
                "completed": completed,
            },
            "progress": ProgressSerializer(progresses, many=True).data
        })

    return Response({
        "parent": {
            "id": parent.id,
            "username": parent.username,
            "email": parent.email,
        },
        "children": children_data,
    })