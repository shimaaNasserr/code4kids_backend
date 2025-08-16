from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('Kid', 'Kid'),
        ('Parent', 'Parent'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Kid')
    phone_number = models.CharField(max_length=20, blank=True, null=True)  
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = 'email'     
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"


class KidParentRelation(models.Model):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name="children_relations", limit_choices_to={'role': 'Parent'})
    kid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                           related_name="parent_relations", limit_choices_to={'role': 'Kid'})

    def __str__(self):
        return f"{self.parent.username} → {self.kid.username}"
    