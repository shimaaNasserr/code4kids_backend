from django.conf import settings
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    image = models.ImageField(upload_to='courses/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    categories = models.ManyToManyField(Category, related_name='courses')

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    kid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'Kid'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)        
    def __str__(self):
        return f"{self.kid.username} enrolled in {self.course.title}"