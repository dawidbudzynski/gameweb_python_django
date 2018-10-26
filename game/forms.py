from constants import YEARS, RATING
from developer.models import Developer
from django.forms import (Form, CharField, ChoiceField, ModelChoiceField, ImageField, ModelMultipleChoiceField,
                          CheckboxSelectMultiple, Select,
                          NullBooleanField)
from genre.models import Genre
from tag.models import Tag

SORTED_YEARS = sorted(YEARS, key=lambda x: x[1])
SORTED_RATING = sorted(RATING, key=lambda x: x[0])

all_tags = Tag.objects.all()
all_developers = Developer.objects.all()
all_genres = Genre.objects.all()


class RateGameForm(Form):
    score = ChoiceField(choices=SORTED_RATING)


class AddGameForm(Form):
    title = CharField(max_length=64)
    year = ChoiceField(choices=SORTED_YEARS)
    developer = ModelChoiceField(queryset=all_developers.order_by('name'),
                                 widget=Select)
    genre = ModelChoiceField(queryset=all_genres.order_by('name'),
                             widget=Select)
    tags = ModelMultipleChoiceField(label='Tags (Select 6)',
                                    queryset=all_tags.order_by('name'),
                                    widget=CheckboxSelectMultiple(attrs={'class': 'checkboxmultiple'}))
    image = ImageField(required=False)
    top_20 = NullBooleanField(label='Is in top 20?', required=False)
