from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
from lessons.models import Lesson
from assignments.models import Assignment, Submission

User = get_user_model()

class Progress(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_progress')
    kid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kid_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.IntegerField(default=0)
    performance_notes = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.kid.username} - {str(self.course)}"

    @property
    def total_lessons_count(self):
        return self.course.lessons.count()
    
    @property
    def total_assignments_count(self):
        return Assignment.objects.filter(lesson__course=self.course).count()
    
    @property
    def completed_assignments_count(self):
        return Submission.objects.filter(
            student=self.kid,
            assignment__lesson__course=self.course,
            grade__isnull=False  # الواجب تم تصحيحه
        ).count()
    
    @property
    def total_course_items(self):
        return self.total_lessons_count + self.total_assignments_count
    
    @property
    def completed_course_items(self):
        completed_lessons = max(0, min(self.completed_lessons, self.total_lessons_count))
        completed_assignments = self.completed_assignments_count
        return completed_lessons + completed_assignments
    
    @property
    def progress_percentage(self):
        total_items = self.total_course_items
        if total_items == 0:
            return 0.0
        
        completed_items = self.completed_course_items
        percentage = (completed_items / total_items) * 100
        return round(percentage, 2)
    
    @property
    def lessons_progress_percentage(self):
        total_lessons = self.total_lessons_count
        if total_lessons == 0:
            return 0.0
        
        completed_lessons = max(0, min(self.completed_lessons, total_lessons))
        percentage = (completed_lessons / total_lessons) * 100
        return round(percentage, 2)
    
    @property
    def assignments_progress_percentage(self):
        total_assignments = self.total_assignments_count
        if total_assignments == 0:
            return 0.0
        
        completed_assignments = self.completed_assignments_count
        percentage = (completed_assignments / total_assignments) * 100
        return round(percentage, 2)
    
    def get_detailed_progress(self):
        return {
            'total_lessons': self.total_lessons_count,
            'completed_lessons': max(0, min(self.completed_lessons, self.total_lessons_count)),
            'total_assignments': self.total_assignments_count,
            'completed_assignments': self.completed_assignments_count,
            'total_items': self.total_course_items,
            'completed_items': self.completed_course_items,
            'overall_percentage': self.progress_percentage,
            'lessons_percentage': self.lessons_progress_percentage,
            'assignments_percentage': self.assignments_progress_percentage,
        }
    
    def update_lesson_progress(self, lessons_completed):
        max_lessons = self.total_lessons_count
        self.completed_lessons = max(0, min(lessons_completed, max_lessons))
        self.save()
        return self.progress_percentage
