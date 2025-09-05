# courses/admin_urls.py - Admin URLs 
from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.admin_course_list_create, name='admin_course_list_create'),
    path('courses/<int:pk>/', views.admin_course_detail, name='admin_course_detail'),
    
    path('instructors/', views.admin_instructor_list_create, name='admin_instructor_list_create'),
    path('instructors/<int:pk>/', views.admin_instructor_detail, name='admin_instructor_detail'),
    
    path('categories/', views.admin_category_list_create, name='admin_category_list_create'),
    path('categories/<int:pk>/', views.admin_category_detail, name='admin_category_detail'),
]