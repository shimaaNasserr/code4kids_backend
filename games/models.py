from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator


class GameCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_ar = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, default='gamepad')  # FontAwesome icon name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Game Categories"
        ordering = ['name']


class Game(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    description_ar = models.TextField(blank=True, null=True)
    
    # Game details
    duration_minutes = models.PositiveIntegerField(
        default=30,
        help_text="Duration in minutes",
        validators=[MinValueValidator(5), MaxValueValidator(180)]
    )
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    
    # Media
    image = CloudinaryField("image", blank=True, null=True)
    game_url = models.URLField(blank=True, null=True, help_text="External game URL")
    
    # Progress tracking
    total_levels = models.PositiveIntegerField(default=10)
    
    # Metadata
    category = models.ForeignKey(GameCategory, on_delete=models.CASCADE, related_name='games')
    skills = models.JSONField(default=list, help_text="List of skills taught")
    rating = models.FloatField(
        default=4.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    player_count = models.CharField(max_length=20, default="1K+", help_text="Display player count")
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'Admin'}
    )

    def __str__(self):
        return self.title

    def get_average_progress(self):
        """Calculate average progress across all players"""
        progresses = self.game_progress.all()
        if not progresses:
            return 0
        return sum(p.completion_percentage for p in progresses) / len(progresses)

    def get_completion_rate(self):
        """Calculate percentage of players who completed the game"""
        total_players = self.game_progress.count()
        if total_players == 0:
            return 0
        completed_players = self.game_progress.filter(completion_percentage=100).count()
        return (completed_players / total_players) * 100

    class Meta:
        ordering = ['order', '-created_at']


class GameProgress(models.Model):
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Kid'},
        related_name='game_progress'
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_progress')
    
    # Progress tracking
    current_level = models.PositiveIntegerField(default=1)
    completion_percentage = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    time_spent_minutes = models.PositiveIntegerField(default=0)
    
    # Achievements
    badges_earned = models.JSONField(default=list)
    high_score = models.PositiveIntegerField(default=0)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    last_played = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['player', 'game']
        ordering = ['-last_played']

    def __str__(self):
        return f"{self.player.username} - {self.game.title} ({self.completion_percentage}%)"

    def is_completed(self):
        return self.completion_percentage >= 100

    def get_completed_levels(self):
        return int((self.completion_percentage / 100) * self.game.total_levels)


class GameSession(models.Model):
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Kid'}
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    # Session data
    session_duration_minutes = models.PositiveIntegerField(default=0)
    levels_completed_in_session = models.PositiveIntegerField(default=0)
    score_earned = models.PositiveIntegerField(default=0)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.username} - {self.game.title} session on {self.started_at.date()}"

    class Meta:
        ordering = ['-started_at']
