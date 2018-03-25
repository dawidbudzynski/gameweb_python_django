from django.contrib.auth.models import User as DjangoUser
from django.db import models

# Create your models here.

YEARS = {(1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997),
         (1998, 1998), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006),
         (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014),
         (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)}


class Genre(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class User(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=None)
    favorite_tags = models.ManyToManyField(Tag, blank=True)
    favorite_genre = models.ManyToManyField(Genre, blank=True)
    favorite_developer = models.ForeignKey(Developer, blank=True, null=True, on_delete=None)


class Game(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(null=True)
    year = models.IntegerField(choices=YEARS)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    genre = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='images/', null=True)
    top_20 = models.NullBooleanField(null=True)


class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(blank=True)
