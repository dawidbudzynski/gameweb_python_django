from django.urls import path

from . import views

app_name = 'game_recommendation'

urlpatterns = [
    path('recommend_game_by_tags', views.RecommendManually.as_view(),
         name='recommend-by-tags'),
    path('recommend_game_by_rating', views.RecommendByRating.as_view(),
         name='recommend-by-rating')
]
