from django.db import models
from courses.models import Course

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)  
    title = models.CharField(max_length=200)                      
    content = models.TextField()      
    is_completed = models.BooleanField(default=False)                         
    video_url = models.URLField(blank=True, null=True)            
    order = models.PositiveIntegerField()   
    description = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        ordering = ['course', 'order']
        unique_together = ['course', 'order']  

    def __str__(self):
        return f"{self.course.title} - {self.title}"