from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from .models import GameCategory, Game, GameProgress, GameSession
from .serializers import (
    GameCategorySerializer, GameSerializer, GameProgressSerializer,
    GameProgressUpdateSerializer, GameSessionSerializer, GameStatsSerializer
)


class GameCategoryListView(generics.ListAPIView):
    """List all game categories"""
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    permission_classes = [permissions.AllowAny]


class GameListView(generics.ListAPIView):
    """List all active games with user progress if authenticated"""
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Game.objects.filter(is_active=True)
        
        # Filter by category if provided
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        
        # Filter by difficulty if provided
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter featured games if requested
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('order', '-created_at')


class GameDetailView(generics.RetrieveAPIView):
    """Get detailed information about a specific game"""
    queryset = Game.objects.filter(is_active=True)
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]


class UserGameProgressListView(generics.ListAPIView):
    """List user's progress across all games"""
    serializer_class = GameProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return GameProgress.objects.filter(player=self.request.user)


class GameProgressDetailView(generics.RetrieveUpdateAPIView):
    """Get or update progress for a specific game"""
    serializer_class = GameProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        game_id = self.kwargs.get('game_id')
        game = get_object_or_404(Game, id=game_id, is_active=True)
        
        # Get or create progress for this user and game
        progress, created = GameProgress.objects.get_or_create(
            player=self.request.user,
            game=game,
            defaults={'current_level': 1, 'completion_percentage': 0}
        )
        return progress
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return GameProgressUpdateSerializer
        return GameProgressSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def start_game_session(request, game_id):
    """Start a new game session"""
    game = get_object_or_404(Game, id=game_id, is_active=True)
    
    # Create new session
    session = GameSession.objects.create(
        player=request.user,
        game=game
    )
    
    serializer = GameSessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def end_game_session(request, session_id):
    """End a game session and update progress"""
    session = get_object_or_404(GameSession, id=session_id, player=request.user)
    
    # Update session data from request
    session.ended_at = timezone.now()
    session.session_duration_minutes = request.data.get('duration_minutes', 0)
    session.levels_completed_in_session = request.data.get('levels_completed', 0)
    session.score_earned = request.data.get('score_earned', 0)
    session.save()
    
    # Update game progress
    progress, created = GameProgress.objects.get_or_create(
        player=request.user,
        game=session.game,
        defaults={'current_level': 1, 'completion_percentage': 0}
    )
    
    # Update progress based on session data
    new_level = request.data.get('current_level', progress.current_level)
    new_percentage = request.data.get('completion_percentage', progress.completion_percentage)
    new_time = progress.time_spent_minutes + session.session_duration_minutes
    new_score = max(progress.high_score, session.score_earned)
    
    progress.current_level = max(progress.current_level, new_level)
    progress.completion_percentage = max(progress.completion_percentage, new_percentage)
    progress.time_spent_minutes = new_time
    progress.high_score = new_score
    
    # Add badges if any
    new_badges = request.data.get('badges_earned', [])
    if new_badges:
        existing_badges = set(progress.badges_earned)
        all_badges = existing_badges.union(set(new_badges))
        progress.badges_earned = list(all_badges)
    
    # Mark as completed if 100%
    if progress.completion_percentage >= 100 and not progress.completed_at:
        progress.completed_at = timezone.now()
    
    progress.save()
    
    return Response({
        'session': GameSessionSerializer(session).data,
        'progress': GameProgressSerializer(progress).data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_game_stats(request):
    """Get comprehensive game statistics for the user"""
    user_progress = GameProgress.objects.filter(player=request.user)
    
    total_games = Game.objects.filter(is_active=True).count()
    games_started = user_progress.count()
    games_completed = user_progress.filter(completion_percentage=100).count()
    total_time_spent = user_progress.aggregate(total=Sum('time_spent_minutes'))['total'] or 0
    total_badges = sum(len(p.badges_earned) for p in user_progress)
    
    # Calculate average rating of played games
    played_games = Game.objects.filter(id__in=user_progress.values_list('game_id', flat=True))
    average_rating = played_games.aggregate(avg=Avg('rating'))['avg'] or 0
    
    # Find favorite category (most played)
    category_stats = user_progress.values('game__category__name').annotate(
        count=Count('id'),
        time=Sum('time_spent_minutes')
    ).order_by('-time')
    
    favorite_category = category_stats.first()['game__category__name'] if category_stats else 'None'
    
    completion_rate = (games_completed / games_started * 100) if games_started > 0 else 0
    
    stats_data = {
        'total_games': total_games,
        'games_started': games_started,
        'games_completed': games_completed,
        'total_time_spent': total_time_spent,
        'total_badges': total_badges,
        'average_rating': round(average_rating, 1),
        'favorite_category': favorite_category,
        'completion_rate': round(completion_rate, 1)
    }
    
    serializer = GameStatsSerializer(stats_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def game_leaderboard(request, game_id):
    """Get leaderboard for a specific game"""
    game = get_object_or_404(Game, id=game_id, is_active=True)
    
    # Get top players by completion percentage and high score
    top_players = GameProgress.objects.filter(game=game).order_by(
        '-completion_percentage', '-high_score', 'time_spent_minutes'
    )[:10]
    
    leaderboard_data = []
    for i, progress in enumerate(top_players, 1):
        leaderboard_data.append({
            'rank': i,
            'player_name': progress.player.username,
            'completion_percentage': progress.completion_percentage,
            'high_score': progress.high_score,
            'time_spent_minutes': progress.time_spent_minutes,
            'badges_count': len(progress.badges_earned)
        })
    
    return Response({
        'game_title': game.title,
        'leaderboard': leaderboard_data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reset_game_progress(request, game_id):
    """Reset user's progress for a specific game"""
    game = get_object_or_404(Game, id=game_id, is_active=True)
    
    try:
        progress = GameProgress.objects.get(player=request.user, game=game)
        progress.current_level = 1
        progress.completion_percentage = 0
        progress.time_spent_minutes = 0
        progress.badges_earned = []
        progress.high_score = 0
        progress.completed_at = None
        progress.save()
        
        return Response({'message': 'Game progress reset successfully'})
    except GameProgress.DoesNotExist:
        return Response({'message': 'No progress found for this game'}, 
                       status=status.HTTP_404_NOT_FOUND)
