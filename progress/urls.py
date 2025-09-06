from django.urls import path
from . import views

urlpatterns = [
    path("child-dashboard/", views.child_dashboard, name="child_dashboard"),
    path("parent-dashboard/", views.parent_dashboard, name="parent_dashboard"),
]
