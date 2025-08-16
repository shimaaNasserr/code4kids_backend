from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('courses/', views.course_list_create, name='course_list_create'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/courses/', views.category_courses, name='category_courses'),
    path('instructors/', views.instructor_list_create, name='instructor_list_create'),
    path('instructors/<int:pk>/', views.instructor_detail, name='instructor_detail'),
    path('enroll/', views.enroll_in_course, name='enroll-in-course'),
    path('my-enrollments/', views.my_enrollments, name='my-enrollments'),
    path('unenroll/', views.unenroll_from_course, name='unenroll-from-course'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    