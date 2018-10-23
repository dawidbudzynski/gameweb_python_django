"""projekt_koncowy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from game_recommendation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.TechNews.as_view(),
         name='mainpage'),
    path('about/', views.AboutPageView.as_view(),
         name='about'),
    path('users/', views.ShowUsersView.as_view(),
         name='users'),
    path('add_user/', views.AddUserView.as_view(),
         name='add-user'),
    path('delete_user/<user_id>', views.DeleteUserView.as_view(),
         name='delete-user'),
    path('tags/', views.ShowTagsView.as_view(),
         name='tags'),
    path('add_tag/', views.AddTagView.as_view(),
         name='add-tag'),
    path('add_genre/', views.AddGenreView.as_view(),
         name='add-genre'),
    path('genres/', views.ShowGenreView.as_view(),
         name='genres'),
    path('add_developer/', views.AddDeveloperView.as_view(),
         name='add-developer'),
    path('developers/', views.ShowDevelopersView.as_view(),
         name='developers'),
    path('add_game/', views.AddGameView.as_view(),
         name='add-game'),
    path('games/', views.ShowGamesView.as_view(),
         name='games'),
    path('delete_game/<game_id>', views.DeleteGameView.as_view(),
         name='delete-game'),
    path('wrong_value', views.WrongValueView.as_view()),
    path('wrong_password', views.WrongPasswordView.as_view()),
    path('login', views.LoginUserView.as_view(),
         name='login'),
    path('logout', views.LogoutUserView.as_view(),
         name='logout'),
    path('object_already_exist', views.ObjectAlreadyExistView.as_view()),
    path('recommend_game_by_tags', views.RecommendManually.as_view(),
         name='recommend-by-tags'),
    path('delete_tag/<tag_id>', views.DeleteTagView.as_view(),
         name='delete-tag'),
    path('delete_genre/<genre_id>', views.DeleteGenreView.as_view(),
         name='delete-genre'),
    path('delete_developer/<developer_pk>', views.DeleteDeveloperView.as_view(),
         name='delete-developer'),
    path('recommend_game_by_rating', views.RecommendByRating.as_view(),
         name='recommend-by-rating'),
    path('show_games_with_tag/<tag_id>', views.ShowAllGamesWithTagView.as_view(),
         name='show-tag'),
    path('show_games_with_genre/<genre_id>', views.ShowAllGamesWithGenreView.as_view(),
         name='show-genre'),
    path('show_games_with_developer/<developer_id>', views.ShowAllGamesWithDeveloperView.as_view(),
         name='show-developer'),
    path(r'tech_news/<news_source>', views.TechNews.as_view(),
         name='tech_news'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
