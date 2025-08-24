from django.contrib import admin
from django.urls import path, include,re_path
from lessons.views import upload_media
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('lessons.urls')),
    path('api/', include('ratings.urls')),
    path('progress/', include('progress.urls')),
    path('upload/', upload_media, name='upload_media'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    # path('accounts/google/login/callback/', google_login_redirect, name="google_login_redirect"),
    path('api/chatbot/', include('chatbot.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
