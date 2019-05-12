from django.forms import (CharField, Form)
from django.utils.translation import ugettext_lazy as _


class AddGenreForm(Form):
    name = CharField(max_length=64, label=_('Name'))
