from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from courses.models import Course
from lessons.models import Lesson, LessonCompletion
from assignments.models import Assignment, Submission
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model()

class Progress(models.Model):
    parent = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='children_progress', null=True, blank=True)
    kid = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE ,related_name="progress_entries")
    completed_lessons = models.IntegerField(default=0) 
    completed_assignments = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        unique_together = ("kid", "course")
        ordering = ["-last_updated"]

    def clean(self):
        # تأكد إن القيم مش أكبر من العدد الكلي
        if self.completed_lessons > self.course.total_lessons:
            raise ValidationError({"completed_lessons": "number of lesson doesnt exceed total lessons"})

        if self.completed_assignments > self.course.total_assignments:
            raise ValidationError({"completed_assignments": "number of assignment doesnt exceed total assignments"})

    def save(self, *args, **kwargs):
        # تنظيف البيانات قبل الحفظ
        self.full_clean()
        super().save(*args, **kwargs)    

    # ✅ دلوقتي بنعتمد على الحقول المباشرة الموجودة في Course
    def total_lessons(self) -> int:
        return self.course.total_lessons

    def total_assignments(self) -> int:
        return self.course.total_assignments

    def progress_percentage(self) -> float:
        total_items = self.total_lessons() + self.total_assignments()
        completed_items = self.completed_lessons + self.completed_assignments
        if total_items == 0:
            return 0.0
        return round((completed_items / total_items) * 100.0, 2)

    def recompute(self, save=True):
        """إعادة حساب التقدم من جداول LessonCompletion و Submission"""
        from lessons.models import LessonCompletion
        from assignments.models import Submission

        self.completed_lessons = LessonCompletion.objects.filter(
            student=self.kid,
            lesson__course=self.course
        ).count()

        self.completed_assignments = Submission.objects.filter(
            student=self.kid,
            assignment__course=self.course
        ).count()

        if save:
            self.save()

    def __str__(self):
        return (
            f"{self.kid.username} | {self.course.title} "
        )