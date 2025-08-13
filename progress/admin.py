from django.contrib import admin
from .models import Progress

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = (
        'kid', 
        'course', 
        'completed_lessons',  
        'total_lessons_count', 
        'completed_assignments_count', 
        'total_assignments_count',
        'progress_percentage', 
        'date'
    )
    
    def total_lessons_count(self, obj):
        return obj.total_lessons_count
    total_lessons_count.short_description = 'Total Lessons'

    def completed_assignments_count(self, obj):
        return obj.completed_assignments_count
    completed_assignments_count.short_description = 'Completed Assignments'

    def total_assignments_count(self, obj):
        return obj.total_assignments_count
    total_assignments_count.short_description = 'Total Assignments'

    def progress_percentage(self, obj):
        return f"{obj.progress_percentage} %"
    progress_percentage.short_description = 'Progress %'