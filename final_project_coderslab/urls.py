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

from game_recommendation.views import (MainPage, AddUserView, ShowUsersView, DeleteUserView,
                                       ShowTagsView, AddTagView, DeleteTagView,
                                       AddGenreView, ShowGenreView, DeleteGenreView,
                                       AddDeveloperView, ShowDevelopersView, DeleteDeveloperView,
                                       AddGameView, ShowGamesView, DeleteGameView,
                                       WrongValueView, ObjectAlreadyExistView, WrongPasswordView,
                                       LoginUserView, LogoutUserView,
                                       RecommendManually, RecommendByRating, ExperienceChoiceView,
                                       APINewsView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', APINewsView.as_view(),
         name='mainpage'),
    path('users/', ShowUsersView.as_view(),
         name='users'),
    path('add_user/', AddUserView.as_view(),
         name='add-user'),
    path('delete_user/<user_id>', DeleteUserView.as_view(),
         name='delete-user'),
    path('tags/', ShowTagsView.as_view(),
         name='tags'),
    path('add_tag/', AddTagView.as_view(),
         name='add-tag'),
    path('add_genre/', AddGenreView.as_view(),
         name='add-genre'),
    path('genres/', ShowGenreView.as_view(),
         name='genres'),
    path('add_developer/', AddDeveloperView.as_view(),
         name='add-developer'),
    path('developers/', ShowDevelopersView.as_view(),
         name='developers'),
    path('add_game/', AddGameView.as_view(),
         name='add-game'),
    path('games/', ShowGamesView.as_view(),
         name='games'),
    path('delete_game/<game_id>', DeleteGameView.as_view(),
         name='delete-game'),
    path('wrong_value', WrongValueView.as_view()),
    path('wrong_password', WrongPasswordView.as_view()),
    path('login', LoginUserView.as_view(),
         name='login'),
    path('logout', LogoutUserView.as_view(),
         name='logout'),
    path('object_already_exist', ObjectAlreadyExistView.as_view()),
    path('recommend_game_by_tags', RecommendManually.as_view(),
         name='recommend-by-tags'),
    path('delete_tag/<tag_id>', DeleteTagView.as_view(),
         name='delete-tag'),
    path('delete_genre/<genre_id>', DeleteGenreView.as_view(),
         name='delete-genre'),
    path('delete_developer/<developer_id>', DeleteDeveloperView.as_view(),
         name='delete-developer'),
    path('recommend_game_by_rating', RecommendByRating.as_view(),
         name='recommend-by-rating'),
    path('experience_level_choice', ExperienceChoiceView.as_view(),
         name='experience-choice'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)