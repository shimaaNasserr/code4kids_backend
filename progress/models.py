from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

from lessons.models import Lesson

User = get_user_model()

class Progress(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_progress')
    kid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kid_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.IntegerField(default=0)
    performance_notes = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.kid.username} - {str(self.course)}"

    @property
    def progress_percentage(self):
        total_lessons = 0
        if hasattr(self.course, 'lessons'):
            total_lessons = self.course.lessons.count()
        if total_lessons <= 0:
            return 0
        completed = max(0, int(self.completed_lessons))
        # امن: ما نخليش completed أكبر من total
        completed = min(completed, total_lessons)
        return round((completed / total_lessons) * 100, 2)
