from django.urls import path
from . import views
from assignments.views import AssignmentsByLessonListAPIView, SubmissionCreateAPIView, SubmissionGradeAPIView

urlpatterns = [
    # Regular lesson endpoints
    path('lessons/', views.lesson_list_create, name='lesson-list-create'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson-detail'),
    path('lessons/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark-lesson-complete'),
    path("lessons/<int:lesson_id>/assignments/", AssignmentsByLessonListAPIView.as_view(), name="assignments-by-lesson"),
    path("submissions/create/", SubmissionCreateAPIView.as_view(), name="submission-create"),
    path("submissions/<int:submission_id>/grade/", SubmissionGradeAPIView.as_view(), name="submission-grade"),
    
    # Admin-specific lesson endpoints
    path('admin/lessons/', views.admin_lesson_list_create, name='admin-lesson-list-create'),
    path('admin/lessons/<int:pk>/', views.admin_lesson_detail, name='admin-lesson-detail'),
    
    # Statistics endpoint
    path('admin/statistics/', views.admin_statistics, name='admin-statistics'),
]
