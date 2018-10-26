from django.urls import path

from . import views

app_name = 'genre'

urlpatterns = [
    path('add_genre/', views.AddGenreView.as_view(),
         name='add-genre'),
    path('genres/', views.ShowGenreView.as_view(),
         name='genres'),
    path('delete_genre/<genre_id>', views.DeleteGenreView.as_view(),
         name='delete-genre'),
    path('show_games_with_genre/<genre_id>', views.ShowAllGamesWithGenreView.as_view(),
         name='show-genre')
]
