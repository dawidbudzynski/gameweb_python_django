from collections import Counter
from operator import itemgetter

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User as DjangoUser
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View

from .forms import (AddUserForm, AddTagForm, AddGenreForm, AddDeveloperForm, LoginUserForm, AddGameForm, ChooseTagsForm)
from .keys import api_key
from .models import (User, Tag, Game, Genre, Developer)


# Create your views here.

# ERRORS

class WrongValueView(View):
    def get(self, request):
        return render(request, template_name='wrong_value_error.html')


class ObjectAlreadyExistView(View):
    def get(self, request):
        return render(request, template_name='object_already_exist.html')


class WrongPasswordView(View):
    def get(self, request):
        return render(request, template_name='wrong_password.html')


class ShowUsersView(View):
    def get(self, request):
        all_users = User.objects.all().order_by('user__username')

        ctx = {'all_users': all_users}

        return render(request,
                      template_name='users.html',
                      context=ctx)


class AddUserView(View):
    def get(self, request):
        form = AddUserForm().as_p()
        ctx = {'form': form}

        return render(request,
                      template_name='add_user.html',
                      context=ctx)

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            if password != password2:
                return HttpResponseRedirect("/wrong_password")
            if DjangoUser.objects.filter(username=username).exists():
                return HttpResponseRedirect('/object_already_exist')

            django_user = DjangoUser.objects.create_user(username=username, password=password,
                                                         first_name=first_name, last_name=last_name, email=email)
            User.objects.create(user=django_user)

            return HttpResponseRedirect('/users')
        return HttpResponseRedirect('/wrong_value')


class DeleteUserView(PermissionRequiredMixin, View):
    permission_required = 'game_recommendation.delete_genre'
    raise_exception = True

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.delete()

        return HttpResponseRedirect('/users')


# TAGS

class ShowTagsView(View):
    def get(self, request):
        all_tags = Tag.objects.all().order_by('name')

        ctx = {'all_tags': all_tags}

        return render(request,
                      template_name='tags.html',
                      context=ctx)


class AddTagView(View):
    def get(self, request):
        form = AddTagForm().as_p()
        ctx = {'form': form}

        return render(request,
                      template_name='add_tag.html',
                      context=ctx)

    def post(self, request):
        form = AddTagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            if Tag.objects.filter(name=name).exists():
                return HttpResponseRedirect('/object_already_exist')

            Tag.objects.create(name=name)

            return HttpResponseRedirect('/tags')
        return HttpResponseRedirect('/wrong_value')


class DeleteTagView(PermissionRequiredMixin, View):
    permission_required = 'game_recommendation.delete_tag'
    raise_exception = True

    def get(self, request, tag_id):
        tag = Tag.objects.get(id=tag_id)
        tag.delete()

        return HttpResponseRedirect('/tags')


# GENRE

class AddGenreView(View):
    def get(self, request):
        form = AddGenreForm().as_p()
        ctx = {'form': form}

        return render(request,
                      template_name='add_genre.html',
                      context=ctx)

    def post(self, request):
        form = AddTagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            if Genre.objects.filter(name=name).exists():
                return HttpResponseRedirect('/object_already_exist')

            Genre.objects.create(name=name)

            return HttpResponseRedirect('/genres')
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

        return HttpResponseRedirect('/genres')


# DEVELOPER

class AddDeveloperView(View):
    def get(self, request):
        form = AddDeveloperForm().as_p()
        ctx = {'form': form}

        return render(request,
                      template_name='add_developer.html',
                      context=ctx)

    def post(self, request):
        form = AddDeveloperForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            if Developer.objects.filter(name=name).exists():
                return HttpResponseRedirect('/object_already_exist')

            Developer.objects.create(name=name)

            return HttpResponseRedirect('/developers')
        return HttpResponseRedirect('/wrong_value')


class DeleteDeveloperView(PermissionRequiredMixin, View):
    permission_required = 'game_recommendation.delete_developer'
    raise_exception = True

    def get(self, request, developer_pk):
        developer = Developer.objects.get(pk=developer_pk)
        print(developer)
        developer.delete()

        return HttpResponseRedirect('/developers')


class ShowDevelopersView(View):
    def get(self, request):
        all_developers = Developer.objects.all().order_by('name')

        ctx = {'all_developers': all_developers}

        return render(request,
                      template_name='developers.html',
                      context=ctx)


# GAMES

class AddGameView(View):
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

            new_game = Game.objects.create(title=title, year=year,
                                           developer=developer, image=image, top_20=top_20)

            new_game.genre.add(genre)

            for tag in tags_list:
                new_game.tags.add(tag)

            return HttpResponseRedirect('/games')
        return HttpResponseRedirect('/wrong_value')


class ShowGamesView(View):
    def get(self, request):
        all_games = Game.objects.all().order_by('title')

        ctx = {'all_games': all_games}

        return render(request,
                      template_name='games.html',
                      context=ctx)


class DeleteGameView(PermissionRequiredMixin, View):
    permission_required = 'game_recommendation.delete_game'
    raise_exception = True

    def get(self, request, game_id):
        game = Game.objects.get(id=game_id)
        game.delete()

        return HttpResponseRedirect('/games')


# LOGIN

class LoginUserView(View):
    def get(self, request):
        loggedUser = request.session.get('loggedUser')
        if loggedUser is None:
            form = LoginUserForm().as_p()
            ctx = {
                'form': form
            }
            print(loggedUser)
            return render(request,
                          template_name='login.html',
                          context=ctx)

        else:
            name_to_display = loggedUser
            del request.session['loggedUser']
            return HttpResponseRedirect('/')

    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            request.session['loggedUser'] = username
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/wrong_password')
        else:
            return HttpResponseRedirect('/wrong_value')


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


# RECOMMENDATIONS

class RecommendManually(LoginRequiredMixin, View):
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
                        match_score += 20
                    elif game_genre.name != genre.name:
                        genre_match = False
                if game_object.developer.name == developer.name:
                    developer_match = True
                    match_score += 20
                elif game_object.developer.name != developer.name:
                    developer_match = False
                for user_tag in game[1]:
                    match_score += 10
                    for game_tag in game_object.tags.all():
                        if user_tag == game_tag.name:
                            matched_tags.append(game_tag)
                        else:
                            unmatched_tags.append(game_tag)

                unmatched_tags = list(set(unmatched_tags) ^ set(matched_tags))

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


class RecommendByRating(LoginRequiredMixin, View):
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
                        match_score += 10
                    else:
                        unmatched_tags.append(game_tag)

            for game_genre in game.genre.all():
                try:
                    if game_genre.name == favorite_genre.name:
                        genre_match = True
                        match_score += 20
                    elif game_genre.name != favorite_genre.name:
                        genre_match = False
                except AttributeError:
                    return HttpResponse('You have to rate more games')

            if game.developer.name == favorite_developer.name:
                developer_match = True
                match_score += 20
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


# APU IGN NEWS

class APINewsView(View):
    def get(self, request):
        url = ('https://newsapi.org/v2/top-headlines?sources=polygon&apiKey={}'.format(api_key))

        response = requests.get(url)

        ctx = {
            'response': response.json()['articles'],
        }
        return render(request,
                      template_name='base.html',
                      context=ctx)
