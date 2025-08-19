# accounts/urls.py
from django.urls import path
from .views import (
    register, loginUser, parent_only_view, kid_only_view, admin_only_view, 
    get_full_user_profile, update_user_profile, add_points,
    profile_dashboard, upload_avatar, course_progress_detail, achievements
)

urlpatterns = [
    # Authentication
    path('register/', register, name='register'),
    path('login/', loginUser, name='login'),
    
    # Role-based views
    path('parent-only/', parent_only_view, name='parent_only'),
    path('kid-only/', kid_only_view, name='kid_only'),
    path('admin-only/', admin_only_view, name='admin_only'),
    
    # Profile - Basic 
    path('profile/', get_full_user_profile, name='get_profile'),
    path('profile/update/', update_user_profile, name='update_profile'),
    path('profile/add-points/', add_points, name='add_points'),
    
    # Profile 
    path('profile/dashboard/', profile_dashboard, name='profile_dashboard'),
    path('profile/avatar/', upload_avatar, name='upload_avatar'),
    path('profile/course/<int:course_id>/', course_progress_detail, name='course_progress'),
    path('profile/achievements/', achievements, name='achievements'),
]