from django.forms import (CharField, EmailField, Form, PasswordInput)


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


class LoginUserForm(Form):
    username = CharField(label='User', strip=True)
    password = CharField(label='Password', widget=PasswordInput)
