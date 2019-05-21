from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic import TemplateView

from .tasks import save_games_to_csv_task


class AboutView(TemplateView):
    template_name = 'about.html'


class DownloadGamesToCSVView(View):

    def get(self, request):
        save_games_to_csv_task.delay()
        messages.add_message(request, messages.INFO, _(
            'Games will be downloaded in background. Come back in few moments'
        ))
        return render(
            request,
            template_name='download_games_to_csv_result.html'
        )
