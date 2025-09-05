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
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)  

    bio = models.TextField(max_length=300, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    
    favorite_language = models.CharField(max_length=50, blank=True, choices=[
        ('Python', 'Python'),
        ('JavaScript', 'JavaScript'), 
        ('Scratch', 'Scratch'),
        ('HTML/CSS', 'HTML/CSS'),
    ])
    skill_level = models.CharField(max_length=20, choices=[
        ('Beginner', 'مبتدئ'),
        ('Intermediate', 'متوسط'),
        ('Advanced', 'متقدم')
    ], default='Beginner')
    
    points = models.IntegerField(default=0)
    courses_completed = models.IntegerField(default=0)
    badges = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
    @property
    def age(self):
        if self.birth_date:
            from datetime import date
            return (date.today() - self.birth_date).days // 365
        return None
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()