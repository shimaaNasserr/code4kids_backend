from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
    
class Instructor(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True, help_text="A brief bio about the instructor")
    specialization = models.CharField(max_length=200, blank=True, null=True, help_text="Specialization")
    years_of_experience = models.PositiveIntegerField(
        default=0, 
        help_text="Years of experience",
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    profile_image = CloudinaryField("image", blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    image = CloudinaryField("image", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    total_lessons = models.IntegerField(default=0)
    total_assignments = models.IntegerField(default=0)
    max_students = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        limit_choices_to={'role': 'Admin'}
    )
    categories = models.ManyToManyField(Category, related_name='courses', blank=True)
    instructors = models.ManyToManyField(
        Instructor, 
        related_name='courses', 
        blank=True, 
        help_text="Instructors responsible for this course"
    )

    def __str__(self):
        return self.title

    def get_instructors_names(self):
        if self.instructors.exists():
            return ", ".join([instructor.name for instructor in self.instructors.all()])
        return "No instructors assigned"

    def get_total_lessons(self):
        return self.lessons.count()

    def get_enrollments_count(self):
        return self.enrollment_set.count()

    class Meta:
        ordering = ['-created_at']

class Enrollment(models.Model):
    kid = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'Kid'}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    completion_percentage = models.FloatField(default=0.0)

    class Meta:
        unique_together = ['kid', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.kid.username} enrolled in {self.course.title}"
    


    # def calculate_progress(self):
    #     total_lessons = self.course.get_total_lessons()
    #     if total_lessons == 0:
    #         return 0.0
        
        # completed_lessons = LessonCompletion.objects.filter(
        #     student=self.kid, 
        #     lesson__course=self.course
        # ).count()
        
        # return (completed_lessons / total_lessons) * 100
        # return 0.0