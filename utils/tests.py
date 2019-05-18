from django.contrib.auth.models import User as DjangoUser

import random

from developer.models import Developer
from game.models import Game
from genre.models import Genre
from tag.models import Tag
from users.models import User


def populate_database():
    django_user = DjangoUser.objects.create(
        username='user_1',
        password='password_1',
        first_name='first_name_1',
        last_name='last_name_1',
        email='email_1'
    )
    User.objects.create(user=django_user)
    for i in range(1, 21):
        Tag.objects.create(name=f'tag_{i}')
        Genre.objects.create(name=f'genre_{i}')
        Developer.objects.create(name=f'developer_{i}')
    for i in range(1, 21):
        Game.objects.create(
            developer=Developer.objects.get(name='developer_{}'.format(random.randint(1, 20))),
            genre=Genre.objects.get(name='genre_{}'.format(random.randint(1, 20))),
            title=f'game_{i}',
            year=random.randint(2000, 2019),
            to_be_rated=random.choice([True, False])
        )
    for game in Game.objects.all():
        for tag in random.choices(list(Tag.objects.all()), k=5):
            game.tags.add(tag)
