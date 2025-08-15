from django.db import models
from lessons.models import Lesson
from django.conf import settings  


class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='assignments', on_delete=models.CASCADE)
    question = models.TextField()
    model_answer = models.TextField(blank=True, null=True)  
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"Assignment for {self.lesson.title}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to="submissions/files/", null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # مثال: 95.50
    feedback = models.TextField(null=True, blank=True)



    class Meta:
        ordering = ["-submitted_at"]
        unique_together = ("assignment", "student")

    def __str__(self):
        return f"Submission by {self.student.username} for {self.assignment.lesson.title}"    

