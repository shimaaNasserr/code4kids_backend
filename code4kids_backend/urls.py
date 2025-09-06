from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts.views import AdminLoginView, ParentLoginView, KidLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('lessons.urls')),
    path('api/', include('ratings.urls')),
    path('api/', include('games.urls')),
    path('api/progress/', include('progress.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    # path('accounts/google/login/callback/', google_login_redirect, name="google_login_redirect"),
    path('api/chatbot/', include('chatbot.urls')),
    # Auth role-specific JWT endpoints
    path('api/accounts/admin/login', AdminLoginView.as_view(), name='admin-login'),
    path('api/accounts/parent/login', ParentLoginView.as_view(), name='parent-login'),
    path('api/accounts/kid/login', KidLoginView.as_view(), name='kid-login'),
    path('api/admin/', include('courses.admin_urls')),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
