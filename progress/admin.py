from django.contrib import admin
from .models import Progress

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = (
        "kid",
        "course",
        "total_lessons",
        "completed_lessons_count",
        "total_assignments",
        "completed_assignments_count",
        "progress_percentage",
        "last_updated",
    )
    search_fields = ("kid__username", "course__title")
    list_filter = ("course", "last_updated", "created_at")  # عدلنا "date" → "created_at"

    # عدد كل الدروس في الكورس
    def total_lessons(self, obj):
        return getattr(obj.course, "total_lessons", 0)
    total_lessons.short_description = "Total Lessons"

    # عدد الدروس اللي خلصها
    def completed_lessons_count(self, obj):
        return obj.completed_lessons  # مباشرة IntegerField
    completed_lessons_count.short_description = "Completed Lessons"

    # عدد كل الأسايمنت في الكورس
    def total_assignments(self, obj):
        return getattr(obj.course, "total_assignments", 0)
    total_assignments.short_description = "Total Assignments"

    # عدد الأسايمنت اللي خلصها
    def completed_assignments_count(self, obj):
        return obj.completed_assignments  # مباشرة IntegerField
    completed_assignments_count.short_description = "Completed Assignments"

    # نسبة التقدم
    def progress_percentage(self, obj):
        total_lessons = getattr(obj.course, "total_lessons", 0)
        total_assignments = getattr(obj.course, "total_assignments", 0)
        total_items = total_lessons + total_assignments

        completed_items = obj.completed_lessons + obj.completed_assignments

        if total_items == 0:
            return "0%"
        return f"{(completed_items / total_items) * 100:.2f}%"
    progress_percentage.short_description = "Progress %"
