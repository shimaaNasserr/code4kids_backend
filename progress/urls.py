from django.urls import path
from .views import (
    # ParentProgressListView, 
    # AdminProgressListView,
    # kid_progress_detail,
    # kid_progress_summary,
    # refresh_progress,
    # add_performance_note,
    child_dashboard,
    parent_dashboard
)

urlpatterns = [
    # path('parent/', ParentProgressListView.as_view(), name='parent-progress'),
    # path('admin/', AdminProgressListView.as_view(), name='admin-progress'),
    # path('kid/<int:kid_id>/', kid_progress_detail, name='kid-progress-detail'),    
    # path('kid/<int:kid_id>/summary/', kid_progress_summary, name='kid-progress-summary'),
    # path('kid/<int:kid_id>/refresh/', refresh_progress, name='refresh-progress'),
    # path('<int:progress_id>/note/', add_performance_note, name='add-performance-note'),
    path("dashboard/child/", child_dashboard, name="child_dashboard"),
    path("dashboard/parent/", parent_dashboard, name="parent_dashboard"),
]
