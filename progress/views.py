from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Progress

# -------------------- CHILD DASHBOARD --------------------
@login_required
def child_dashboard(request):
    user = request.user
    if user.role != "Kid":
        return JsonResponse({"error": "Only kids can access this endpoint"}, status=403)

    progress_data = []
    progresses = Progress.objects.filter(kid=user)  # ✅ استخدمي kid مش user (زي موديلك)

    for p in progresses:
        progress_data.append({
            "course": p.course.title,
            "total_lessons": p.course.lessons.count(),
            "completed_lessons": p.completed_lessons,   # ✅ شيل .count()
            "total_assignments": p.course.assignments.count(),
            "completed_assignments": p.completed_assignments,  # ✅ شيل .count()
            "progress_percentage": p.progress_percentage(),
        })

    return JsonResponse({
        "child": user.username,
        "progress": progress_data
    })


# -------------------- PARENT DASHBOARD --------------------
@login_required
def parent_dashboard(request):
    user = request.user
    if user.role != "Parent":
        return JsonResponse({"error": "Only parents can access this endpoint"}, status=403)

    children_data = []
    children = user.children.all()  # assuming you have a related_name='children' in Kid model

    for child in children:
        child_progresses = Progress.objects.filter(kid=child)  # ✅ برضه خليها kid
        progress_data = []
        for p in child_progresses:
            progress_data.append({
                "course": p.course.title,
                "total_lessons": p.course.lessons.count(),
                "completed_lessons": p.completed_lessons,   # ✅
                "total_assignments": p.course.assignments.count(),
                "completed_assignments": p.completed_assignments,  # ✅
                "progress_percentage": p.progress_percentage(),
            })

        children_data.append({
            "child": child.username,
            "progress": progress_data
        })

    return JsonResponse({
        "parent": user.username,
        "children_progress": children_data
    })
