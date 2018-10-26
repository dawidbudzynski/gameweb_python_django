from django.forms import (Form, CharField)


class AddTagForm(Form):
    name = CharField(max_length=64)
