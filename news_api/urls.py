from django.urls import path

from . import views

app_name = 'news_api'

urlpatterns = [
    path(r'', views.TechNews.as_view(),
         name='mainpage'),
    path(r'show_news/<news_source>', views.TechNews.as_view(),
         name='show-news'),
]
