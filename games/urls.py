from django.urls import path
from . import views

urlpatterns = [
    # Game categories
    path('categories/', views.GameCategoryListView.as_view(), name='game-categories'),
    
    # Games
    path('games/', views.GameListView.as_view(), name='games-list'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
    
    # User progress
    path('my-progress/', views.UserGameProgressListView.as_view(), name='user-game-progress'),
    path('games/<int:game_id>/progress/', views.GameProgressDetailView.as_view(), name='game-progress'),
    path('games/<int:game_id>/reset/', views.reset_game_progress, name='reset-game-progress'),
    
    # Game sessions
    path('games/<int:game_id>/start-session/', views.start_game_session, name='start-game-session'),
    path('sessions/<int:session_id>/end/', views.end_game_session, name='end-game-session'),
    
    # Statistics and leaderboards
    path('my-stats/', views.user_game_stats, name='user-game-stats'),
    path('games/<int:game_id>/leaderboard/', views.game_leaderboard, name='game-leaderboard'),
]
