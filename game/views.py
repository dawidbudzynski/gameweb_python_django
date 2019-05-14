from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic import ListView
from users.models import User

from .forms import AddGameForm, RateGameForm
from .models import Game, GameScore


class GameListView(ListView):
    model = Game
    template_name = 'game_list.html'


class GameCreateView(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {'form': AddGameForm().as_p()}

        return render(
            request,
            template_name='game_create.html',
            context=ctx
        )

    def post(self, request):
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            year = form.cleaned_data['year']
            developer = form.cleaned_data['developer']
            genre = form.cleaned_data['genre']
            tags = form.cleaned_data['tags']
            image = form.cleaned_data['image']
            to_be_rated = form.cleaned_data['to_be_rated']

            tags_list = [tag for tag in tags] if tags else []

            if Game.objects.filter(title=title).exists():
                messages.add_message(request, messages.WARNING, _('Game with this name already exists'))
                return HttpResponseRedirect(reverse('game:game-create'))

            new_game = Game.objects.create(
                title=title,
                year=year,
                developer=developer,
                genre=genre,
                image=image,
                to_be_rated=to_be_rated
            )

            for tag in tags_list:
                new_game.tags.add(tag)

            messages.add_message(request, messages.INFO, _('Game: {} created successfully').format(title))
            return HttpResponseRedirect(reverse('game:game-list'))

        messages.add_message(request, messages.ERROR, _('Form invalid'))
        return HttpResponseRedirect(reverse('game:game-create'))


class GameDetails(View):
    def get(self, request, game_id):
        """Display single game details with form for rating"""
        game = Game.objects.get(id=game_id)
        try:
            user = User.objects.get(id=request.user.id)
            gamescore = GameScore.objects.get(game=game, user=user)
        except ObjectDoesNotExist:
            gamescore = None

        ctx = {'game': game,
               'gamescore': gamescore,
               'form': RateGameForm()}

        return render(
            request,
            template_name='game_details.html',
            context=ctx
        )

    def post(self, request, game_id):
        """Get rating from form and create or update gamescore"""
        form = RateGameForm(request.POST)
        try:
            user = User.objects.get(user=request.user)
        except User.DoesNotExist:
            messages.add_message(request, messages.INFO, _('User {} can\'t rate games').format(request.user))
            return HttpResponseRedirect(reverse('game:game-list'))
        game = Game.objects.get(id=game_id)
        try:
            old_gamescore = GameScore.objects.get(game=game, user=user)
        except GameScore.DoesNotExist:
            old_gamescore = None
        if form.is_valid():
            score = form.cleaned_data['score']
            if old_gamescore is not None:
                old_gamescore.score = score
                old_gamescore.save()
                gamescore = old_gamescore
            else:
                gamescore = GameScore.objects.create(
                    user=user,
                    game=game,
                    score=score
                )

        ctx = {'game': game,
               'form': form,
               'gamescore': gamescore}

        return render(
            request,
            template_name='game_details.html',
            context=ctx
        )


class GameDeleteView(PermissionRequiredMixin, View):
    """Delete game"""
    permission_required = 'game_recommendation.delete_game'
    raise_exception = True

    def get(self, request, game_id):
        game = Game.objects.get(id=game_id)
        game.delete()
        return HttpResponseRedirect(reverse('game:game-list'))
