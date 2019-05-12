from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('game_create/', views.GameCreateView.as_view(),
         name='game-create'),
    path('game_list/', views.GameListView.as_view(),
         name='game-list'),
    path('game_details/<game_id>', views.GameDetails.as_view(),
         name='game-details'),
    path('game_delete/<game_id>', views.GameDeleteView.as_view(),
         name='game-delete'),
]
