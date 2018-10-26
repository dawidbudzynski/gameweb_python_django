from django.urls import path

from . import views

app_name = 'tag'

urlpatterns = [
    path('tags/', views.ShowTagsView.as_view(),
         name='tags'),
    path('add_tag/', views.AddTagView.as_view(),
         name='add-tag'),
    path('delete_tag/<tag_id>', views.DeleteTagView.as_view(),
         name='delete-tag'),
    path('show_games_with_tag/<tag_id>', views.ShowAllGamesWithTagView.as_view(),
         name='show-tag')
]
