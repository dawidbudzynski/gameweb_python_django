from django.forms import (Form, CharField)


class AddGenreForm(Form):
    name = CharField(max_length=64)
