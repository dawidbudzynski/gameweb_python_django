from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('users/', views.ShowUsersView.as_view(),
         name='users'),
    path('add_user/', views.AddUserView.as_view(),
         name='add-user'),
    path('delete_user/<user_id>', views.DeleteUserView.as_view(),
         name='delete-user'),
    path('login', views.LoginUserView.as_view(),
         name='login'),
    path('logout', views.LogoutUserView.as_view(),
         name='logout'),
]
