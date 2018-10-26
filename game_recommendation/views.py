from collections import Counter
from operator import itemgetter

from constants import (DEVELOPER_MATCH,
                       GENRE_MATCH,
                       TAG_MATCH)
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from game.models import Game

from .forms import (ChooseTagsForm)


# Create your views here.

class RecommendManually(View):
    def get(self, request):
        form = ChooseTagsForm().as_p()
        ctx = {
            'form': form
        }
        return render(request,
                      template_name='choose_preferences.html',
                      context=ctx)

    def post(self, request):
        form = ChooseTagsForm(request.POST)
        if form.is_valid():

            genre = form.cleaned_data['genre']
            developer = form.cleaned_data['developer']
            tags = form.cleaned_data['tags']

            all_games_all_information = []
            all_games_with_common_tags = []
            sorted_all_game_information = []
            user_favorites = {}

            if tags:
                selected_tags = [tag.name for tag in tags]
            else:
                selected_tags = []

            all_games = Game.objects.all()
            for game in all_games:
                game_tag_list = []
                for tag in game.tags.all():
                    game_tag_list.append(tag.name)
                common_tags = list(set(game_tag_list).intersection(selected_tags))

                result = [game.title, common_tags]
                all_games_with_common_tags.append(result)

            for game in all_games_with_common_tags:
                single_game_information = {}
                genre_match = None
                developer_match = None
                matched_tags = []
                unmatched_tags = []
                match_score = 0
                game_object = Game.objects.get(title=game[0])
                for game_genre in game_object.genre.all():
                    if game_genre.name == genre.name:
                        genre_match = True
                        match_score += GENRE_MATCH
                    elif game_genre.name != genre.name:
                        genre_match = False
                if game_object.developer.name == developer.name:
                    developer_match = True
                    match_score += DEVELOPER_MATCH
                elif game_object.developer.name != developer.name:
                    developer_match = False
                for user_tag in game[1]:
                    match_score += TAG_MATCH
                    for game_tag in game_object.tags.all():
                        if user_tag == game_tag.name:
                            matched_tags.append(game_tag)
                        else:
                            unmatched_tags.append(game_tag)

                if len(matched_tags) > 0:
                    unmatched_tags = list(set(unmatched_tags) ^ set(matched_tags))
                else:
                    unmatched_tags = list(set(unmatched_tags))

                single_game_information.update(
                    {'game': game_object, 'genre_match': genre_match, 'developer_match': developer_match,
                     'match_score': match_score, 'matched_tags': matched_tags,
                     'unmatched_tags': unmatched_tags})
                all_games_all_information.append(single_game_information)

                sorted_all_game_information = sorted(all_games_all_information, key=itemgetter('match_score'))
                sorted_all_game_information.reverse()

            user_favorites.update({'favorite_tags_top_6': tags, 'favorite_genre': genre,
                                   'favorite_developer': developer})

            ctx = {
                'sorted_all_game_information': sorted_all_game_information,
                'user_favorites': user_favorites
            }

            return render(request,
                          template_name='recommendations_by_tags_result.html',
                          context=ctx)
        return HttpResponseRedirect('/wrong_value')


class RecommendByRating(View):
    def get(self, request):
        games_top_20 = Game.objects.filter(top_20=True)

        ctx = {
            'games_top_20': games_top_20
        }
        return render(request,
                      template_name='rate_games_form.html',
                      context=ctx)

    def post(self, request):
        games_top_20 = Game.objects.filter(top_20=True)
        all_games = Game.objects.all()

        games_not_rated = list(set(all_games) - set(games_top_20))

        all_games_all_information = []
        sorted_all_game_information = []
        liked_games = []
        disliked_games = []
        liked_tags = []
        favorite_tags_top_6 = []
        liked_genres = []
        favorite_genre = None
        liked_developers = []
        favorite_developer = None
        user_favorites = {}

        # sorting games: liked or disliked

        for game in games_top_20:
            like_or_dislike = request.POST["game_{}".format(game.id)]
            if like_or_dislike == 'like':
                liked_games.append(game)
            elif like_or_dislike == 'dislike':
                disliked_games.append(game)

        for game in liked_games:
            for tag in game.tags.all():
                liked_tags.append(tag)
                try:
                    for genre in game.genre.all():
                        liked_genres.append(genre)
                    liked_developers.append(game.developer)
                except AttributeError:
                    return HttpResponseRedirect('/wrong_value')

        # looking for top 6 favorites tags
        tags_counted = Counter(liked_tags)
        tag_items = tags_counted.items()
        sorted_tags = sorted(tag_items, key=lambda x: x[1], reverse=True)[:6]
        for element in sorted_tags:
            favorite_tags_top_6.append(element[0])

        # looking for top 1 favorites genres
        genres_counted = Counter(liked_genres)
        genre_items = genres_counted.items()
        sorted_genres = sorted(genre_items, key=lambda x: x[1], reverse=True)[:1]
        for element in sorted_genres:
            favorite_genre = element[0]

        # looking for top 1 favorites developers
        developers_counted = Counter(liked_developers)
        developers_items = developers_counted.items()
        sorted_developers = sorted(developers_items, key=lambda x: x[1], reverse=True)[:1]
        for element in sorted_developers:
            favorite_developer = element[0]

        for game in games_not_rated:
            single_game_all_information = {}
            matched_tags = []
            unmatched_tags = []
            genre_match = None
            developer_match = None
            match_score = 0
            for user_tag in favorite_tags_top_6:
                for game_tag in game.tags.all():
                    if user_tag.name == game_tag.name:
                        matched_tags.append(game_tag)
                        match_score += TAG_MATCH
                    else:
                        unmatched_tags.append(game_tag)

            for game_genre in game.genre.all():
                try:
                    if game_genre.name == favorite_genre.name:
                        genre_match = True
                        match_score += GENRE_MATCH
                    elif game_genre.name != favorite_genre.name:
                        genre_match = False
                except AttributeError:
                    return HttpResponse('You have to rate more games')

            if game.developer.name == favorite_developer.name:
                developer_match = True
                match_score += DEVELOPER_MATCH
            elif game.developer.name != favorite_developer.name:
                developer_match = False

            unmatched_tags = list(set(unmatched_tags) ^ set(matched_tags))

            single_game_all_information.update({'game': game, 'matched_tags': matched_tags,
                                                'unmatched_tags': unmatched_tags, 'match_score': match_score,
                                                'genre_match': genre_match, 'developer_match': developer_match})
            all_games_all_information.append(single_game_all_information)

            sorted_all_game_information = sorted(all_games_all_information, key=itemgetter('match_score'))
            sorted_all_game_information.reverse()
        user_favorites.update({'favorite_tags_top_6': favorite_tags_top_6, 'favorite_genre': favorite_genre,
                               'favorite_developer': favorite_developer})
        print(games_not_rated)
        ctx = {
            'sorted_all_game_information': sorted_all_game_information,
            'user_favorites': user_favorites
        }

        return render(request,
                      template_name='recommendations_by_rating.html',
                      context=ctx)
