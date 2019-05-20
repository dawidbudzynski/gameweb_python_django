import csv
import os
import time
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic import TemplateView

from game.models import Game


class AboutView(TemplateView):
    template_name = 'about.html'


class DownloadGamesToCSVView(View):

    def get(self, request):
        start = time.clock()
        self._save_games_to_csv()
        elapsed = time.clock()
        download_time = elapsed - start
        messages.add_message(request, messages.INFO, _('Games downloaded to CSV successfully'))
        ctx = {'download_time': download_time}
        return render(
            request,
            template_name='download_games_to_csv_result.html',
            context=ctx
        )

    @staticmethod
    def _save_games_to_csv():
        all_games = Game.objects.all()
        with open(os.path.join(settings.MEDIA_ROOT, 'csv', 'game_data.csv'), 'w') as filepath:
            writer = csv.DictWriter(
                filepath,
                fieldnames=['time', 'title', 'developer', 'genre', 'year'],
                delimiter=';'
            )
            writer.writeheader()
            for game in all_games:
                # creating big CSV file to test Celary
                for i in range(4000):
                    writer.writerow({
                        'time': datetime.now(),
                        'title': game.title,
                        'developer': game.developer.name,
                        'genre': game.genre.name,
                        'year': game.year
                    })
