from django.urls import path

from . import views

app_name = 'developer'

urlpatterns = [
    path('add_developer/', views.AddDeveloperView.as_view(),
         name='add-developer'),
    path('developers/', views.ShowDevelopersView.as_view(),
         name='developers'),
    path('delete_developer/<developer_pk>', views.DeleteDeveloperView.as_view(),
         name='delete-developer'),
    path('show_games_with_developer/<developer_id>', views.ShowAllGamesWithDeveloperView.as_view(),
         name='show-developer')
]
