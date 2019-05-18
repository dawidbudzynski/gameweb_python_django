from django.urls import path

from . import views

app_name = 'news_api'

urlpatterns = [
    path('', views.TechNewsView.as_view(),
         name='mainpage'),
    path('show_news/<news_source>', views.TechNewsView.as_view(),
         name='show-news'),
]
