from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
from lessons.models import Lesson, LessonCompletion
from assignments.models import Assignment, Submission
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

User = get_user_model()

class Progress(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_progress')
    kid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kid_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.IntegerField(default=0)
    completed_assignments = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    total_assignments = models.IntegerField(default=0)
    performance_notes = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.kid.username} - {str(self.course)}"

    @property
    def total_activities(self):
        return self.total_lessons + self.total_assignments

    @property
    def completed_activities(self):
        return self.completed_lessons + self.completed_assignments

    @property
    def progress_percentage(self):
        if self.total_activities <= 0:
            return 0
        
        completed = max(0, self.completed_activities)
        completed = min(completed, self.total_activities)
        return round((completed / self.total_activities) * 100, 2)

    def calculate_actual_progress(self):
        actual_completed_lessons = LessonCompletion.objects.filter(
            student=self.kid,
            lesson__course=self.course
        ).count()

        actual_completed_assignments = Submission.objects.filter(
            student=self.kid,
            assignment__lesson__course=self.course,
            grade__isnull=False
        ).count()

        actual_total_lessons = self.course.lessons.count()
        actual_total_assignments = Assignment.objects.filter(lesson__course=self.course).count()

        return {
            'completed_lessons': actual_completed_lessons,
            'completed_assignments': actual_completed_assignments,
            'total_lessons': actual_total_lessons,
            'total_assignments': actual_total_assignments,
        }

    def update_progress(self):
        actual = self.calculate_actual_progress()
        self.completed_lessons = actual['completed_lessons']
        self.completed_assignments = actual['completed_assignments']
        self.total_lessons = actual['total_lessons']
        self.total_assignments = actual['total_assignments']
        self.save()

    @property
    def lessons_progress_percentage(self):
        if self.total_lessons <= 0:
            return 0
        return round((self.completed_lessons / self.total_lessons) * 100, 2)

    @property
    def assignments_progress_percentage(self):
        """نسبة تقدم التكليفات فقط."""
        if self.total_assignments <= 0:
            return 0
        return round((self.completed_assignments / self.total_assignments) * 100, 2)

    class Meta:
        unique_together = ['kid', 'course']
        ordering = ['-last_updated']


def get_parent_of_kid(kid):
    from accounts.models import KidParentRelation
    try:
        relation = KidParentRelation.objects.filter(kid=kid).first()
        return relation.parent if relation else None
    except:
        return None


@receiver(post_save, sender=LessonCompletion)
def update_progress_on_lesson_completion(sender, instance, created, **kwargs):
    if created:
        progress, _ = Progress.objects.get_or_create(
            kid=instance.student,
            course=instance.lesson.course,
            defaults={
                'parent': get_parent_of_kid(instance.student)
            }
        )
        progress.update_progress()

@receiver(post_delete, sender=LessonCompletion)
def update_progress_on_lesson_deletion(sender, instance, **kwargs):
    try:
        progress = Progress.objects.get(
            kid=instance.student,
            course=instance.lesson.course
        )
        progress.update_progress()
    except Progress.DoesNotExist:
        pass

@receiver(post_save, sender=Submission)
def update_progress_on_assignment_submission(sender, instance, created, **kwargs):
    if instance.grade is not None:
        progress, _ = Progress.objects.get_or_create(
            kid=instance.student,
            course=instance.assignment.lesson.course,
            defaults={
                'parent': get_parent_of_kid(instance.student)
            }
        )
        progress.update_progress()