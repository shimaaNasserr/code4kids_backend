from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from lessons.models import LessonCompletion
from assignments.models import Submission
from .models import Progress


def update_progress(student, course):
    progress, created = Progress.objects.get_or_create(
        kid=student,   
        course=course
    )
    progress.recompute()


@receiver([post_save, post_delete], sender=LessonCompletion)
def lesson_completion_handler(sender, instance, **kwargs):
    update_progress(instance.student, instance.lesson.course) 


@receiver([post_save, post_delete], sender=Submission)
def submission_handler(sender, instance, **kwargs):
    update_progress(instance.student, instance.assignment.lesson.course) 
