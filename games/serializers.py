from rest_framework import serializers
from .models import GameCategory, Game, GameProgress, GameSession
from accounts.models import User


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameCategory
        fields = ['id', 'name', 'name_ar', 'description', 'description_ar', 'icon']


class GameSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_name_ar = serializers.CharField(source='category.name_ar', read_only=True)
    image_url = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = [
            'id', 'title', 'title_ar', 'description', 'description_ar',
            'duration_minutes', 'difficulty', 'image_url', 'game_url',
            'total_levels', 'category', 'category_name', 'category_name_ar',
            'skills', 'rating', 'player_count', 'is_featured', 'progress'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
    
    def get_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'Kid':
            try:
                game_progress = GameProgress.objects.get(player=request.user, game=obj)
                return {
                    'completion_percentage': game_progress.completion_percentage,
                    'current_level': game_progress.current_level,
                    'completed_levels': game_progress.get_completed_levels(),
                    'time_spent_minutes': game_progress.time_spent_minutes,
                    'badges_earned': game_progress.badges_earned,
                    'high_score': game_progress.high_score,
                    'is_completed': game_progress.is_completed(),
                    'last_played': game_progress.last_played
                }
            except GameProgress.DoesNotExist:
                pass
        
        return {
            'completion_percentage': 0,
            'current_level': 1,
            'completed_levels': 0,
            'time_spent_minutes': 0,
            'badges_earned': [],
            'high_score': 0,
            'is_completed': False,
            'last_played': None
        }


class GameProgressSerializer(serializers.ModelSerializer):
    game_title = serializers.CharField(source='game.title', read_only=True)
    game_title_ar = serializers.CharField(source='game.title_ar', read_only=True)
    player_username = serializers.CharField(source='player.username', read_only=True)
    completed_levels = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    
    class Meta:
        model = GameProgress
        fields = [
            'id', 'game', 'game_title', 'game_title_ar', 'player', 'player_username',
            'current_level', 'completion_percentage', 'completed_levels', 'time_spent_minutes',
            'badges_earned', 'high_score', 'is_completed', 'started_at', 'last_played', 'completed_at'
        ]
        read_only_fields = ['started_at', 'last_played']
    
    def get_completed_levels(self, obj):
        return obj.get_completed_levels()
    
    def get_is_completed(self, obj):
        return obj.is_completed()


class GameProgressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameProgress
        fields = [
            'current_level', 'completion_percentage', 'time_spent_minutes',
            'badges_earned', 'high_score'
        ]
    
    def validate_completion_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Completion percentage must be between 0 and 100.")
        return value
    
    def validate_current_level(self, value):
        if value < 1:
            raise serializers.ValidationError("Current level must be at least 1.")
        return value


class GameSessionSerializer(serializers.ModelSerializer):
    game_title = serializers.CharField(source='game.title', read_only=True)
    player_username = serializers.CharField(source='player.username', read_only=True)
    
    class Meta:
        model = GameSession
        fields = [
            'id', 'game', 'game_title', 'player', 'player_username',
            'session_duration_minutes', 'levels_completed_in_session', 'score_earned',
            'started_at', 'ended_at'
        ]
        read_only_fields = ['started_at']


class GameStatsSerializer(serializers.Serializer):
    total_games = serializers.IntegerField()
    games_started = serializers.IntegerField()
    games_completed = serializers.IntegerField()
    total_time_spent = serializers.IntegerField()
    total_badges = serializers.IntegerField()
    average_rating = serializers.FloatField()
    favorite_category = serializers.CharField()
    completion_rate = serializers.FloatField()
