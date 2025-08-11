from django.urls import path
from .views import ParentProgressListView, AdminProgressListView

urlpatterns = [
    path('parent/', ParentProgressListView.as_view(), name='parent-progress'),
    path('admin/', AdminProgressListView.as_view(), name='admin-progress'),
]
