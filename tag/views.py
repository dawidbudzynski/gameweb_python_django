from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic import ListView
from game.models import Game

from .forms import AddTagForm
from .models import Tag


class TagListView(ListView):
    model = Tag
    template_name = 'tag_list.html'


class TagCreateView(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {'form': AddTagForm().as_p()}

        return render(
            request,
            template_name='tag_create.html',
            context=ctx
        )

    def post(self, request):
        form = AddTagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            if Tag.objects.filter(name=name).exists():
                messages.add_message(request, messages.WARNING, _('Tag with this name already exists'))
                return HttpResponseRedirect(reverse('tag:tag-create'))

            Tag.objects.create(name=name)
            messages.add_message(request, messages.INFO, _('Tag: {} created successfully').format(name))
            return HttpResponseRedirect(reverse('tag:tag-list'))

        messages.add_message(request, messages.ERROR, _('Form invalid'))
        return HttpResponseRedirect(reverse('tag:tag-create'))


class TagDeleteView(PermissionRequiredMixin, View):
    permission_required = 'game_recommendation.delete_tag'
    raise_exception = True

    def get(self, request, tag_id):
        tag = Tag.objects.get(id=tag_id)
        tag.delete()

        return HttpResponseRedirect(reverse('tag:tag-list'))


class GamesByTagView(View):
    def get(self, request, tag_id):
        """Display all games with selected tag"""
        selected_tag = Tag.objects.get(id=tag_id)

        ctx = {'all_games_with_tag': Game.objects.filter(tags=selected_tag),
               'selected_tag': selected_tag}

        return render(
            request,
            template_name='all_games_with_selected_tag.html',
            context=ctx
        )
