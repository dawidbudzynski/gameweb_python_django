from decouple import config
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from game.models import Game

from .forms import AddDeveloperForm
from .models import Developer

NEWS_API_KEY = config('NEWS_API_KEY', cast=str)


# Create your views here.

class AddDeveloperView(LoginRequiredMixin, View):
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

            return HttpResponseRedirect('/developer/developers')
        return HttpResponseRedirect('/wrong_value')


class DeleteDeveloperView(PermissionRequiredMixin, View):
    permission_required = 'developer.delete_developer'
    raise_exception = True

    def get(self, request, developer_pk):
        developer = Developer.objects.get(pk=developer_pk)
        developer.delete()

        return HttpResponseRedirect('/developers')


class ShowDevelopersView(View):
    def get(self, request):
        all_developers = Developer.objects.all().order_by('name')

        ctx = {'all_developers': all_developers}

        return render(request,
                      template_name='developers.html',
                      context=ctx)


class ShowAllGamesWithDeveloperView(View):
    """Display all games with selected developer"""

    def get(self, request, developer_id):
        selected_developer = Developer.objects.get(id=developer_id)
        all_games_with_developer = Game.objects.filter(developer=selected_developer)

        ctx = {'all_games_with_developer': all_games_with_developer,
               'selected_developer': selected_developer}

        return render(request,
                      template_name='all_games_with_selected_developer.html',
                      context=ctx)
