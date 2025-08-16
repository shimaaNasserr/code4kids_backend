from django.urls import path
from .views import ( register, loginUser, parent_only_view, kid_only_view, admin_only_view, instructor_only_view, get_user_profile,
    update_instructor_profile, list_instructors
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', loginUser, name='login'),
    path('parent-only/', parent_only_view, name='parent_only'),
    path('kid-only/', kid_only_view, name='kid_only'),
    path('admin-only/', admin_only_view, name='admin_only'),
    path('instructor-only/', instructor_only_view, name='instructor_only'),
    path('instructor/profile/', update_instructor_profile, name='update_instructor_profile'),
    path('instructors/', list_instructors, name='list_instructors'),
    path('profile/', get_user_profile, name='profile'),
]
