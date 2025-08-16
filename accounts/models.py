from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False )
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('Kid', 'Kid'),
        ('Parent', 'Parent'),
        ('Admin', 'Admin'),
        ('Instructor', 'Instructor'), 
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Kid')
    phone_number = models.CharField(max_length=20, blank=True, null=True)  
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    bio = models.TextField(blank=True, null=True, help_text="A brief bio about the instructor")
    specialization = models.CharField(max_length=200, blank=True, null=True, help_text="Specialization")
    years_of_experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    profile_image = models.ImageField(upload_to='instructors/', blank=True, null=True)

    USERNAME_FIELD = 'email'     
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"


class KidParentRelation(models.Model):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="children_relations", limit_choices_to={'role': 'Parent'})
    kid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parent_relations", limit_choices_to={'role': 'Kid'})

    def __str__(self):
        return f"{self.parent.username} → {self.kid.username}"

