from decouple import config
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from game.models import Game

from .forms import AddGenreForm
from .models import Genre

NEWS_API_KEY = config('NEWS_API_KEY', cast=str)


# Create your views here.

class AddGenreView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddGenreForm().as_p()
        ctx = {'form': form}

        return render(request,
                      template_name='add_genre.html',
                      context=ctx)

    def post(self, request):
        form = AddGenreForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            if Genre.objects.filter(name=name).exists():
                return HttpResponseRedirect('/object_already_exist')

            Genre.objects.create(name=name)

            return HttpResponseRedirect('genre/genres')
        return HttpResponseRedirect('/wrong_value')


class ShowGenreView(View):
    def get(self, request):
        all_genres = Genre.objects.all().order_by('name')

        ctx = {'all_genres': all_genres}

        return render(request,
                      template_name='genres.html',
                      context=ctx)


class DeleteGenreView(PermissionRequiredMixin, View):
    permission_required = 'game_recommendation.delete_genre'
    raise_exception = True

    def get(self, request, genre_id):
        genre = Genre.objects.get(id=genre_id)
        genre.delete()

        return HttpResponseRedirect('genre/genres')


class ShowAllGamesWithGenreView(View):
    """Display all games with selected genre"""

    def get(self, request, genre_id):
        selected_genre = Genre.objects.get(id=genre_id)
        all_games_with_genre = Game.objects.filter(genre=selected_genre)

        ctx = {'all_games_with_genre': all_games_with_genre,
               'selected_genre': selected_genre}

        return render(request,
                      template_name='all_games_with_selected_genre.html',
                      context=ctx)
