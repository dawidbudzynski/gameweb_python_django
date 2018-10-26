from django.urls import path

from . import views

app_name = 'main_app'

urlpatterns = [
    path('about/', views.AboutPageView.as_view(),
         name='about'),
    path('wrong_value', views.WrongValueView.as_view()),
    path('wrong_password', views.WrongPasswordView.as_view()),
    path('object_already_exist', views.ObjectAlreadyExistView.as_view()),
]
