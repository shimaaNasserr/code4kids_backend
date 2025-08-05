from django.db import models
from lessons.models import Lesson
from django.conf import settings  

class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='assignments', on_delete=models.CASCADE)
    kid = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assignments', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)  
    submitted = models.BooleanField(default=False)    
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assignment for {self.lesson.title} by {self.kid.username}"
