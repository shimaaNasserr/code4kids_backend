from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Course, Category

User = get_user_model()

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'created_by', 'created_at')
    list_filter = ('level', 'created_by')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',) # many2many

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["queryset"] = User.objects.filter(role='Admin')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Course, CourseAdmin)
admin.site.register(Category)