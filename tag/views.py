from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from game.models import Game

from .forms import AddTagForm
from .models import Tag


# Create your views here.

class ShowTagsView(View):
    def get(self, request):
        all_tags = Tag.objects.all().order_by('name')

        ctx = {'all_tags': all_tags}

        return render(request,
                      template_name='tags.html',
                      context=ctx)


class TagCreateView(LoginRequiredMixin, View):
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

            return HttpResponseRedirect('tag/tags')
        return HttpResponseRedirect('/wrong_value')


class DeleteTagView(PermissionRequiredMixin, View):
    permission_required = 'game_recommendation.delete_tag'
    raise_exception = True

    def get(self, request, tag_id):
        tag = Tag.objects.get(id=tag_id)
        tag.delete()

        return HttpResponseRedirect('tag/tags')


class ShowAllGamesWithTagView(View):
    def get(self, request, tag_id):
        """Display all games with selected tag"""
        selected_tag = Tag.objects.get(id=tag_id)
        all_games_with_tag = Game.objects.filter(tags=selected_tag)

        ctx = {'all_games_with_tag': all_games_with_tag,
               'selected_tag': selected_tag}

        return render(request,
                      template_name='all_games_with_selected_tag.html',
                      context=ctx)
