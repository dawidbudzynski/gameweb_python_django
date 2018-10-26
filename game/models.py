from constants import YEARS, RATING
from developer.models import Developer
from django.db import models
from genre.models import Genre
from tag.models import Tag
from users.models import User

SORTED_YEARS = sorted(YEARS, key=lambda x: x[1])
SORTED_RATING = sorted(RATING, key=lambda x: x[0])


class Game(models.Model):
    title = models.CharField(max_length=64)
    year = models.IntegerField(choices=SORTED_YEARS)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    genre = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='images/', blank=True)
    top_20 = models.NullBooleanField(null=True)

    def __str__(self):
        return self.title


class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(choices=SORTED_RATING, blank=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.user, self.game, self.score)
