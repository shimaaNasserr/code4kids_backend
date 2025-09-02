from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/child/", views.child_dashboard, name="child_dashboard"),
    path("dashboard/parent/", views.parent_dashboard, name="parent_dashboard"),
]
