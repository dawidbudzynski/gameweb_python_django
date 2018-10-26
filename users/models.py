from django.contrib.auth.models import User as DjangoUser
from django.db import models


# Create your models here.

class User(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=None)
    favorite_tags = models.ManyToManyField('tag.Tag', blank=True)
    favorite_genre = models.ManyToManyField('genre.Genre', blank=True)
    favorite_developer = models.ForeignKey('developer.Developer', blank=True, null=True, on_delete=None)

    def __str__(self):
        return self.user.username
