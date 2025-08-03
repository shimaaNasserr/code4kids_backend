from django.urls import path
from .views import register, loginUser, parent_only_view, kid_only_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', loginUser, name='login'),
    path('parent-only/', parent_only_view, name='parent_only'),
    path('kid-only/', kid_only_view, name='kid_only'),
]
