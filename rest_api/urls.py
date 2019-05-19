from django.conf.urls import include, url
from rest_framework import routers

from . import views

app_name = 'rest_api'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'users')
router.register(r'games', views.GameViewSet, 'games')
router.register(r'developers', views.DeveloperViewSet, 'developers')
router.register(r'genres', views.GenreViewSet, 'genres')
router.register(r'tags', views.TagViewSet, 'tags')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-main/', views.RestApiMain.as_view(), name='api-main'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
