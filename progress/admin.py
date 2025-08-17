from django.contrib import admin
from .models import Progress
from accounts.models import User  

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = (
        'kid', 'course', 'completed_lessons', 'completed_assignments', 
        'total_lessons_display', 'total_assignments_display', 
        'progress_percentage_display', 'last_updated'
    )
    list_filter = ('course', 'last_updated', 'date')
    search_fields = ('kid__username', 'course__title', 'parent__username')
    readonly_fields = ('progress_percentage_display', 'total_lessons_display', 'total_assignments_display')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = User.objects.filter(role='Parent')
        if db_field.name == "kid":
            kwargs["queryset"] = User.objects.filter(role='Kid')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def total_lessons_display(self, obj):
        return obj.total_lessons
    total_lessons_display.short_description = 'Total Lessons'

    def total_assignments_display(self, obj):
        return obj.total_assignments
    total_assignments_display.short_description = 'Total Assignments'

    def progress_percentage_display(self, obj):
        return f"{obj.progress_percentage}%"
    progress_percentage_display.short_description = 'Progress %'
    
    actions = ['refresh_selected_progress']
    
    def refresh_selected_progress(self, request, queryset):
        updated_count = 0
        for progress in queryset:
            progress.update_progress()
            updated_count += 1
        
        self.message_user(
            request, 
            f"Successfully updated {updated_count} progress records."
        )
    
    refresh_selected_progress.short_description = "Automatically update selected progress"