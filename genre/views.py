from decouple import config
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic import ListView
from game.models import Game

from .forms import AddGenreForm
from .models import Genre

NEWS_API_KEY = config('NEWS_API_KEY', cast=str)


class GenreListView(ListView):
    model = Genre
    template_name = 'genre_list.html'


class GenreCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            template_name='genre_create.html',
            context={'form': AddGenreForm().as_p()}
        )

    def post(self, request):
        form = AddGenreForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            if Genre.objects.filter(name=name).exists():
                messages.add_message(request, messages.WARNING, _('Genre with this name already exists'))
                return HttpResponseRedirect(reverse('genre:genre-create'))

            Genre.objects.create(name=name)
            messages.add_message(request, messages.INFO, _('Genre: {} created successfully').format(name))
            return HttpResponseRedirect(reverse('genre:genre-list'))

        messages.add_message(request, messages.ERROR, _('Form invalid'))
        return HttpResponseRedirect(reverse('genre:genre-create'))


class GenreDeleteView(PermissionRequiredMixin, View):
    permission_required = 'genre.delete_genre'
    raise_exception = True

    def get(self, request, genre_id):
        genre = Genre.objects.get(id=genre_id)
        genre.delete()
        return HttpResponseRedirect(reverse('genre:genre-list'))


class GamesByGenreView(View):
    """Display all games with selected genre"""

    def get(self, request, genre_id):
        selected_genre = Genre.objects.get(id=genre_id)
        ctx = {
            'all_games_with_genre': Game.objects.filter(genre=selected_genre),
            'selected_genre': selected_genre
        }

        return render(
            request,
            template_name='games_by_genre.html',
            context=ctx
        )
