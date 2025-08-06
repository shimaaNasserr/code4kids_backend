from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list_create, name='course_list_create'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/courses/', views.category_courses, name='category_courses'),
]
