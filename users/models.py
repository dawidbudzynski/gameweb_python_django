from django.contrib.auth.models import User as DjangoUser
from django.db import models


class User(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=None)
    favorite_tags = models.ManyToManyField('tag.Tag', blank=True)
    favorite_genre = models.ForeignKey('genre.Genre', blank=True, null=True, on_delete=None)
    favorite_developer = models.ForeignKey('developer.Developer', blank=True, null=True, on_delete=None)

    def __str__(self):
        return self.user.username
