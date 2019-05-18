from django.urls import path

from . import views

app_name = 'game_recommendation'

urlpatterns = [
    path('recommend_game_manually', views.RecommendGamesManuallyView.as_view(),
         name='recommend-manually'),
    path('recommend_game_by_rating', views.RecommendByRatedGamesView.as_view(),
         name='recommend-by-rating')
]
