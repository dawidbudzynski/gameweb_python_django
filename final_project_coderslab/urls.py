import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = []

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include("news_api.urls", namespace="news_api-mainpage")),
    path('developer/', include("developer.urls", namespace="developer")),
    path('game/', include("game.urls", namespace="game")),
    path('genre/', include("genre.urls", namespace="genre")),
    path('main_app/', include("main_app.urls", namespace="main_app")),
    path('news_api/', include("news_api.urls", namespace="news_api")),
    path('recommendation/', include("game_recommendation.urls", namespace="game_recommendation")),
    path('tag/', include("tag.urls", namespace="tag")),
    path('users/', include("users.urls", namespace="users")),
    path('rest_api/', include("rest_api.urls", namespace="rest_api"))
)
if settings.DEBUG:
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
