from django.forms import (Form, CharField, ChoiceField, ModelChoiceField, PasswordInput,
                          ImageField, ModelMultipleChoiceField, CheckboxSelectMultiple, Select,
                          EmailField, NullBooleanField)

from .models import Tag, Developer, Genre

YEARS = {(1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995),
         (1996, 1996), (1997, 1997), (1998, 1998), (2000, 2000), (2001, 2001), (2002, 2002),
         (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008),
         (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014),
         (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)}

RATING = {(1, '1 star'),
          (2, '2 star'),
          (3, '3 star'),
          (4, '4 star'),
          (5, '5 star'),
          (6, '6 star'),
          (7, '7 star'),
          (8, '8 star'),
          (9, '9 star'),
          (10, '10 star')}

SORTED_YEARS = sorted(YEARS, key=lambda x: x[1])
SORTED_RATING = sorted(RATING, key=lambda x: x[0])

all_tags = Tag.objects.all()
all_developers = Developer.objects.all()
all_genres = Genre.objects.all()


class AddUserForm(Form):
    username = CharField(label='Username', strip=True)
    password = CharField(label='Password', widget=PasswordInput)
    first_name = CharField(label='First Name', strip=True, required=False)
    last_name = CharField(label='Surname', strip=True, required=False)
    email = EmailField(label='Email', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Required'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Required'})


class AddTagForm(Form):
    name = CharField(max_length=64)


class AddGenreForm(Form):
    name = CharField(max_length=64)


class AddDeveloperForm(Form):
    name = CharField(max_length=64)


class RateGameForm(Form):
    score = ChoiceField(choices=SORTED_RATING)


class AddGameForm(Form):
    title = CharField(max_length=64)
    year = ChoiceField(choices=SORTED_YEARS)
    developer = ModelChoiceField(queryset=all_developers.order_by('name'),
                                 widget=Select)
    genre = ModelChoiceField(queryset=all_genres.order_by('name'),
                             widget=Select)
    tags = ModelMultipleChoiceField(label='Tags (Select 6)', queryset=all_tags.order_by('name'),
                                    widget=CheckboxSelectMultiple(attrs={'class': 'checkboxmultiple'}))
    image = ImageField()
    top_20 = NullBooleanField(label='Is in top 20?', required=False)


class LoginUserForm(Form):
    username = CharField(label='User', strip=True)
    password = CharField(label='Password', widget=PasswordInput)


class ChooseTagsForm(Form):
    genre = ModelChoiceField(queryset=all_genres.order_by('name'),
                             widget=Select)
    developer = ModelChoiceField(queryset=all_developers.order_by('name'),
                                 widget=Select)
    tags = ModelMultipleChoiceField(label='Tags (Select 6)', queryset=all_tags.order_by('name'),
                                    widget=CheckboxSelectMultiple(attrs={'class': 'checkboxmultiple'}))
