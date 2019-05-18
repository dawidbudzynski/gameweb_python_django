from django.forms import (CharField, CheckboxSelectMultiple, ChoiceField, Form, ImageField, ModelChoiceField,
                          ModelMultipleChoiceField, NullBooleanField, Select)

from constants import SORTED_RATING, SORTED_YEARS
from django.utils.translation import ugettext_lazy as _
from developer.models import Developer
from genre.models import Genre
from tag.models import Tag

all_tags = Tag.objects.all()
all_developers = Developer.objects.all()
all_genres = Genre.objects.all()


class RateGameForm(Form):
    score = ChoiceField(choices=SORTED_RATING)


class AddGameForm(Form):
    title = CharField(max_length=64)
    year = ChoiceField(choices=SORTED_YEARS)
    developer = ModelChoiceField(
        queryset=all_developers.order_by('name'),
        widget=Select
    )
    genre = ModelChoiceField(
        queryset=all_genres.order_by('name'),
        widget=Select
    )
    tags = ModelMultipleChoiceField(
        label=_('Tags (Select 6)'),
        queryset=all_tags.order_by('name'),
        widget=CheckboxSelectMultiple(attrs={'class': 'checkboxmultiple'})
    )
    image = ImageField(required=False)
    to_be_rated = NullBooleanField(label=_('Should be rated?'), required=False)
