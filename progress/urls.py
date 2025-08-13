from django.urls import path
from .views import (
    ParentProgressListView, 
    AdminProgressListView,
    get_kid_progress,
    update_lesson_progress,
    get_detailed_progress
)

urlpatterns = [
    path('parent/', ParentProgressListView.as_view(), name='parent-progress'),
    path('admin/', AdminProgressListView.as_view(), name='admin-progress'),
    path('course/<int:course_id>/', get_kid_progress, name='kid-progress'),
    path('course/<int:course_id>/update-lessons/', update_lesson_progress, name='update-lesson-progress'),
    path('course/<int:course_id>/details/', get_detailed_progress, name='detailed-progress'),
]
