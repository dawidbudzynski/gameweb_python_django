from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('add_game/', views.AddGameView.as_view(),
         name='add-game'),
    path('games/', views.ShowGamesView.as_view(),
         name='games'),
    path('game_details/<game_id>', views.SingeGameDetails.as_view(),
         name='game-details'),
    path('delete_game/<game_id>', views.DeleteGameView.as_view(),
         name='delete-game'),
]
