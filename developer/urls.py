from django.urls import path

from . import views

app_name = 'developer'

urlpatterns = [
    path('developer_create/', views.DeveloperCreateView.as_view(),
         name='developer-create'),
    path('developers/', views.DeveloperListView.as_view(),
         name='developer-list'),
    path('delete_developer/<developer_id>', views.DeveloperDeleteView.as_view(),
         name='delete-developer'),
    path('show_games_with_developer/<developer_id>', views.ShowAllGamesWithDeveloperView.as_view(),
         name='show-developer')
]
