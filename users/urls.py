from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('user_list/', views.UserListView.as_view(),
         name='user_list'),
    path('user_create/', views.UserCreateView.as_view(),
         name='user-create'),
    path('user_delete/<user_id>', views.UserDeleteView.as_view(),
         name='user-delete'),
    path('login', views.LoginView.as_view(),
         name='login'),
    path('logout', views.LogoutView.as_view(),
         name='logout'),
]
