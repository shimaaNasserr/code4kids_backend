from django.db import models
from courses.models import Course
from django.conf import settings

class Lesson(models.Model):
    course = models.ForeignKey(Course,related_name='lessons', on_delete=models.CASCADE)  
    title = models.CharField(max_length=200)                      
    content = models.TextField()      
    is_completed = models.BooleanField(default=False)                         
    video_url = models.URLField(blank=True, null=True)            
    order = models.PositiveIntegerField()   
    description = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)  

    instructors = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    related_name='lessons_taught',
    limit_choices_to={'role': 'Instructor'},
    blank=True,
    help_text="The instructors responsible for this lesson"
)
    class Meta:
        ordering = ['course', 'order']
        unique_together = ['course', 'order']  

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_instructors_names(self):
        return ", ".join([instructor.username for instructor in self.instructors.all()])
    