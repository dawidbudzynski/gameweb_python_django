from django.urls import path

from . import views

app_name = 'genre'

urlpatterns = [
    path('genre_create/', views.GenreCreateView.as_view(),
         name='genre-create'),
    path('genre_list/', views.GenreListView.as_view(),
         name='genre-list'),
    path('genre_delete/<genre_id>', views.GenreDeleteView.as_view(),
         name='genre-delete'),
    path('games_by_genre/<genre_id>', views.GamesByGenreView.as_view(),
         name='games-by-genre')
]
