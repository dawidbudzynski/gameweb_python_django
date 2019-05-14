from django.db import models

from constants import SORTED_RATING, SORTED_YEARS
from developer.models import Developer
from genre.models import Genre
from tag.models import Tag
from users.models import User


class Game(models.Model):
    title = models.CharField(max_length=64)
    year = models.IntegerField(choices=SORTED_YEARS)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='images/', blank=True)
    to_be_rated = models.NullBooleanField(null=True, default=False)

    def __str__(self):
        return self.title


class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(choices=SORTED_RATING, blank=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.user, self.game, self.score)
