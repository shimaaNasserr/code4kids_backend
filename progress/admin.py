from django.contrib import admin
from .models import Progress

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('kid', 'course', 'completed_lessons', 'total_lessons_display', 'progress_percentage_display', 'date')

    def total_lessons_display(self, obj):
        return obj.course.lessons.count() if hasattr(obj.course, 'lessons') else 0
    total_lessons_display.short_description = 'Total lessons'

    def progress_percentage_display(self, obj):
        return f"{obj.progress_percentage} %"
    progress_percentage_display.short_description = 'Progress %'
