import csv
import os
from datetime import datetime

from celery.decorators import periodic_task, task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings

from game.models import Game

logger = get_task_logger(__name__)


def save_games_to_csv(filename):
    all_games = Game.objects.all()
    with open(os.path.join(settings.MEDIA_ROOT, 'csv', filename), 'w') as filepath:
        writer = csv.DictWriter(
            filepath,
            fieldnames=['time', 'title', 'developer', 'genre', 'year'],
            delimiter=';'
        )
        writer.writeheader()
        for game in all_games:
            writer.writerow({
                'time': datetime.now(),
                'title': game.title,
                'developer': game.developer.name,
                'genre': game.genre.name,
                'year': game.year
            })
    logger.info("Games downloaded to CSV successfully")


@task(name="save_games_to_csv_task")
def save_games_to_csv_task():
    """Saves all games to CSV file in background"""
    save_games_to_csv('game_data.csv')


@periodic_task(
    run_every=crontab(minute=0, hour=0),
    name="save_games_to_csv_backup",
    ignore_result=True
)
def save_games_backup():
    """Saves all games to CSV file everyday at midnight"""
    save_games_to_csv('game_data_backup.csv')
