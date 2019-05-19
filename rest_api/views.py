from django.contrib.auth.models import User
from django.views.generic import TemplateView
from developer.models import Developer
from game.models import Game
from genre.models import Genre
from rest_framework import viewsets
from tag.models import Tag

from .serializers import DeveloperSerializer, GameSerializer, GenreSerializer, TagSerializer, UserSerializer


class RestApiMain(TemplateView):
    template_name = 'rest_api_main.html'


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user objects to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class DeveloperViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows developer objects to be viewed or edited.
    """
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows genre objects to be viewed or edited.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tag objects to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows game objects to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
