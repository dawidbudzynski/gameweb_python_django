from django.urls import path

from . import views

app_name = 'tag'

urlpatterns = [
    path('tag_list/', views.TagListView.as_view(),
         name='tag-list'),
    path('tag_create/', views.TagCreateView.as_view(),
         name='tag-create'),
    path('tag_delete/<tag_id>', views.TagDeleteView.as_view(),
         name='tag-delete'),
    path('games_by_tag/<tag_id>', views.GamesByTagView.as_view(),
         name='games-by-tag')
]
