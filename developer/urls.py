from django.urls import path

from . import views

app_name = 'developer'

urlpatterns = [
    path('developer_create/', views.DeveloperCreateView.as_view(),
         name='developer-create'),
    path('developer_list/', views.DeveloperListView.as_view(),
         name='developer-list'),
    path('developer_delete/<developer_id>', views.DeveloperDeleteView.as_view(),
         name='developer-delete'),
    path('games_by_developer/<developer_id>', views.GamesByDeveloperView.as_view(),
         name='games-by-developer')
]
