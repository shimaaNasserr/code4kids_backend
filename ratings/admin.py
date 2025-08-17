from django.contrib import admin
from .models import CourseRating, LessonRating, InstructorRating


@admin.register(CourseRating)
class CourseRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'course']
    search_fields = ['user__username', 'course__title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(LessonRating)
class LessonRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'get_course', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'lesson__course']
    search_fields = ['user__username', 'lesson__title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_course(self, obj):
        return obj.lesson.course.title if obj.lesson and obj.lesson.course else 'N/A'
    get_course.short_description = 'Course'


@admin.register(InstructorRating)
class InstructorRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'instructor', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'instructor']
    search_fields = ['user__username', 'instructor__name', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']