from django.contrib import admin
from django.urls import path , include
from lessons.views import upload_media
from django.conf import settings
from django.conf.urls.static import static
from assignments.views import AssignmentsByLessonListAPIView, SubmissionCreateAPIView, SubmissionGradeAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('lessons.urls')),
    path('progress/', include('progress.urls')),
    path("lessons/<int:lesson_id>/assignments/", AssignmentsByLessonListAPIView.as_view(), name="assignments-by-lesson"),
    path("submissions/create/", SubmissionCreateAPIView.as_view(), name="submission-create"),
    path("submissions/<int:submission_id>/grade/", SubmissionGradeAPIView.as_view(), name="submission-grade"),
    path('upload/', upload_media, name='upload_media'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)