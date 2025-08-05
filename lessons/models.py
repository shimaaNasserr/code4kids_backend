from django.db import models
from courses.models import Course

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  
    title = models.CharField(max_length=200)                      
    content = models.TextField()                               
    video_url = models.URLField(blank=True, null=True)            
    order = models.PositiveIntegerField()                        

    def __str__(self):
        return f"{self.title}"
