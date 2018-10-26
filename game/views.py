from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from users.models import User

from .forms import AddGameForm, RateGameForm
from .models import Game, GameScore


# Create your views here.

class AddGameView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddGameForm().as_p()
        ctx = {'form': form}

        return render(request,
                      template_name='add_game.html',
                      context=ctx)

    def post(self, request):
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            year = form.cleaned_data['year']
            developer = form.cleaned_data['developer']
            genre = form.cleaned_data['genre']
            tags = form.cleaned_data['tags']
            image = form.cleaned_data['image']
            top_20 = form.cleaned_data['top_20']

            tags_list = []
            if tags:
                for tag in tags:
                    tags_list.append(tag)
            else:
                tags_list = []

            if Game.objects.filter(title=title).exists():
                return HttpResponseRedirect('/object_already_exist')

            new_game = Game.objects.create(title=title,
                                           year=year,
                                           developer=developer,
                                           image=image,
                                           top_20=top_20)

            new_game.genre.add(genre)

            for tag in tags_list:
                new_game.tags.add(tag)

            return HttpResponseRedirect('game/games')
        return HttpResponseRedirect('/wrong_value')


class SingeGameDetails(View):
    def get(self, request, game_id):
        """Display single game details with form for rating"""
        game = Game.objects.get(id=game_id)
        try:
            user = User.objects.get(id=request.user.id)
            gamescore = GameScore.objects.get(game=game, user=user)
        except ObjectDoesNotExist:
            gamescore = None
        form = RateGameForm()

        ctx = {'game': game,
               'gamescore': gamescore,
               'form': form}

        return render(request,
                      template_name='game_details.html',
                      context=ctx)

    def post(self, request, game_id):
        """Get rating from form and create or update gamescore"""
        form = RateGameForm(request.POST)
        try:
            user = User.objects.get(id=request.user.id)
            game = Game.objects.get(id=game_id)
            old_gamescore = GameScore.objects.get(game=game, user=user)
        except ObjectDoesNotExist:
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

        return render(request,
                      template_name='game_details.html',
                      context=ctx)


class ShowGamesView(View):
    def get(self, request):
        """Display all games in database"""
        all_games = Game.objects.all().order_by('title')

        ctx = {'all_games': all_games}

        return render(request,
                      template_name='games.html',
                      context=ctx)


class DeleteGameView(PermissionRequiredMixin, View):
    """Delete game"""
    permission_required = 'game_recommendation.delete_game'
    raise_exception = True

    def get(self, request, game_id):
        game = Game.objects.get(id=game_id)
        game.delete()

        return HttpResponseRedirect('game/games')
