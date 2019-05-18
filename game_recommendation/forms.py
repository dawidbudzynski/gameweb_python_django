from django.forms import (CheckboxSelectMultiple, Form, ModelChoiceField, ModelMultipleChoiceField, Select)
from django.utils.translation import ugettext_lazy as _

from developer.models import Developer
from genre.models import Genre
from tag.models import Tag

all_tags = Tag.objects.all()
all_developers = Developer.objects.all()
all_genres = Genre.objects.all()


class ChooseTagsForm(Form):
    genre = ModelChoiceField(
        queryset=all_genres.order_by('name'),
        widget=Select
    )
    developer = ModelChoiceField(
        queryset=all_developers.order_by('name'),
        widget=Select
    )
    tags = ModelMultipleChoiceField(
        label=_('Tags (Select 6)'),
        queryset=all_tags.order_by('name'),
        widget=CheckboxSelectMultiple(attrs={'class': 'checkboxmultiple'})
    )
