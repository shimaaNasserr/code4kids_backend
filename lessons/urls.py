from django.urls import path
from . import views
from assignments.views import AssignmentsByLessonListAPIView, SubmissionCreateAPIView, SubmissionGradeAPIView

urlpatterns = [
    path('lessons/', views.lesson_list_create, name='lesson-list-create'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson-detail'),
    path('lessons/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark-lesson-complete'),
    path("lessons/<int:lesson_id>/assignments/", AssignmentsByLessonListAPIView.as_view(), name="assignments-by-lesson"),
    path("submissions/create/", SubmissionCreateAPIView.as_view(), name="submission-create"),
    path("submissions/<int:submission_id>/grade/", SubmissionGradeAPIView.as_view(), name="submission-grade"),
]
