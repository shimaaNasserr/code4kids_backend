from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Course, Category, Enrollment, Instructor

User = get_user_model()

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'years_of_experience', 'email')
    list_filter = ('specialization', 'years_of_experience')
    search_fields = ('name', 'email', 'specialization')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'created_by', 'get_instructors_display', 'created_at')
    list_filter = ('level', 'created_by', 'instructors')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories', 'instructors')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["queryset"] = User.objects.filter(role='Admin')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_instructors_display(self, obj):
        """Display instructors for this course in admin"""
        instructors = obj.instructors.all()
        if instructors:
            return ", ".join([instructor.name for instructor in instructors])
        return "No instructors assigned"
    get_instructors_display.short_description = 'Instructors'


admin.site.register(Course, CourseAdmin)
admin.site.register(Category)
admin.site.register(Enrollment)