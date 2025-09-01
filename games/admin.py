from django.contrib import admin
from .models import GameCategory, Game, GameProgress, GameSession


@admin.register(GameCategory)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'icon', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'name_ar', 'description']
    ordering = ['name']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'duration_minutes', 'rating', 'is_active', 'is_featured', 'order', 'created_at']
    list_filter = ['difficulty', 'category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'title_ar', 'description']
    list_editable = ['is_active', 'is_featured', 'order']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'title_ar', 'description', 'description_ar', 'category')
        }),
        ('Game Details', {
            'fields': ('difficulty', 'duration_minutes', 'total_levels', 'skills', 'game_url')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Metadata', {
            'fields': ('rating', 'player_count', 'order')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('System', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        })
    )


@admin.register(GameProgress)
class GameProgressAdmin(admin.ModelAdmin):
    list_display = ['player', 'game', 'completion_percentage', 'current_level', 'time_spent_minutes', 'last_played']
    list_filter = ['game', 'completion_percentage', 'started_at', 'last_played']
    search_fields = ['player__username', 'player__email', 'game__title']
    readonly_fields = ['started_at', 'last_played']
    ordering = ['-last_played']


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['player', 'game', 'session_duration_minutes', 'levels_completed_in_session', 'score_earned', 'started_at']
    list_filter = ['game', 'started_at']
    search_fields = ['player__username', 'game__title']
    readonly_fields = ['started_at', 'ended_at']
    ordering = ['-started_at']
