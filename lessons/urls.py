from django.urls import path
from . import views

urlpatterns = [
    path('lessons/', views.lesson_list_create, name='lesson-list-create'),
        path('lessons/<int:pk>/', views.lesson_detail, name='lesson-detail'),
]
