from django.forms import (Form, CharField)


class AddDeveloperForm(Form):
    name = CharField(max_length=64)
