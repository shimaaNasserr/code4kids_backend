from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False )
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('Kid', 'Kid'),
        ('Parent', 'Parent'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='kid')
    phone_number = models.CharField(max_length=20, blank=True, null=True)  
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = 'email'     
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"
