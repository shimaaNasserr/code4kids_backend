from django.urls import path
from . import views

urlpatterns = [
    path('courses/<int:course_id>/ratings/', views.course_rating_list_create, name='course-rating-list-create'),
    path('courses/<int:course_id>/ratings/<int:rating_id>/', views.course_rating_detail, name='course-rating-detail'),
    path('courses/<int:course_id>/ratings/stats/', views.course_rating_stats, name='course-rating-stats'),
    path('lessons/<int:lesson_id>/ratings/', views.lesson_rating_list_create, name='lesson-rating-list-create'),
    path('lessons/<int:lesson_id>/ratings/<int:rating_id>/', views.lesson_rating_detail, name='lesson-rating-detail'),
    path('lessons/<int:lesson_id>/ratings/stats/', views.lesson_rating_stats, name='lesson-rating-stats'),
    path('instructors/<int:instructor_id>/ratings/', views.instructor_rating_list_create, name='instructor-rating-list-create'),
    path('instructors/<int:instructor_id>/ratings/<int:rating_id>/', views.instructor_rating_detail, name='instructor-rating-detail'),
    path('instructors/<int:instructor_id>/ratings/stats/', views.instructor_rating_stats, name='instructor-rating-stats'), 
    path('my-ratings/', views.user_ratings, name='user-ratings'),
]