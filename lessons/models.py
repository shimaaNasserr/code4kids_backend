from django.db import models
from django.conf import settings
from courses.models import Course

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=0, help_text="Duration in minutes")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course', 'order']
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def is_completed_by_user(self, user):
        return LessonCompletion.objects.filter(
            student=user,
            lesson=self
        ).exists()

class LessonCompletion(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Kid'},
        related_name='completed_lessons'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='completions'
    )
    completed_at = models.DateTimeField(auto_now_add=True)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['student', 'lesson']
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.student.username} completed {self.lesson.title}"

class LessonView(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Kid'}
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    duration_watched = models.PositiveIntegerField(default=0, help_text="Duration watched in seconds")

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.student.username} viewed {self.lesson.title}"