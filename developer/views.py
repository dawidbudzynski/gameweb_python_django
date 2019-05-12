from decouple import config
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic.list import ListView
from game.models import Game

from .forms import AddDeveloperForm
from .models import Developer

NEWS_API_KEY = config('NEWS_API_KEY', cast=str)


class DeveloperListView(ListView):
    model = Developer
    template_name = 'developer_list.html'


class DeveloperCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddDeveloperForm().as_p()
        ctx = {'form': form}

        return render(
            request,
            template_name='developer_create.html',
            context=ctx
        )

    def post(self, request):
        form = AddDeveloperForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            if Developer.objects.filter(name=name).exists():
                messages.add_message(request, messages.WARNING, _('Developer with this name already exists'))
                return HttpResponseRedirect(reverse('developer:developer-create'))

            Developer.objects.create(name=name)
            messages.add_message(request, messages.INFO, _('Developer: {} created successfully').format(name))
            return HttpResponseRedirect(reverse('developer:developer-list'))

        messages.add_message(request, messages.ERROR, _('Form invalid'))
        return HttpResponseRedirect(reverse('developer:developer-create'))


class DeveloperDeleteView(PermissionRequiredMixin, View):
    permission_required = 'developer.delete_developer'
    raise_exception = True

    def get(self, request, developer_id):
        developer = Developer.objects.get(id=developer_id)
        developer.delete()
        messages.add_message(request, messages.WARNING, _('Developer: {} has been deleted').format(developer.name))
        return HttpResponseRedirect(reverse('developer:developer-list'))


class GamesByDeveloperView(View):
    """Display all games with selected developer"""

    def get(self, request, developer_id):
        selected_developer = Developer.objects.get(id=developer_id)
        ctx = {
            'all_games_with_developer': Game.objects.filter(developer=selected_developer),
            'selected_developer': selected_developer
        }

        return render(
            request,
            template_name='games_by_developer.html',
            context=ctx
        )
