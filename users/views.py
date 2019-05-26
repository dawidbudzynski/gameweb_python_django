from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as DjangoUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View

from .forms import AddUserForm, LoginUserForm
from .models import User


class UserListView(View):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.add_message(request, messages.WARNING, _('Sorry, you can\'t do that'))
            return HttpResponseRedirect(reverse('news_api:mainpage'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(
            request,
            template_name='user_list.html',
            context={'all_users': User.objects.all().order_by('user__username')}
        )


class UserCreateView(View):

    def get(self, request):
        return render(
            request,
            template_name='user_create.html',
            context={'form': AddUserForm().as_p()}
        )

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            if DjangoUser.objects.filter(username=username).exists():
                messages.add_message(request, messages.WARNING, _('User with this name already exists'))
                return HttpResponseRedirect(reverse('users:user-create'))

            django_user = DjangoUser.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            User.objects.create(user=django_user)
            messages.add_message(request, messages.INFO, _('User: {} created successfully').format(username))
            return HttpResponseRedirect(reverse('users:user_list'))

        messages.add_message(request, messages.ERROR, _('Form invalid'))
        return HttpResponseRedirect(reverse('users:user-create'))


class UserDeleteView(View):

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.add_message(request, messages.WARNING, _('Sorry, you can\'t do that'))
            return HttpResponseRedirect(reverse('news_api:mainpage'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponseRedirect(reverse('users:user-list'))


class LoginView(View):
    def get(self, request):
        if request.session.get('loggedUser') is None:
            return render(
                request,
                template_name='user_login.html',
                context={'form': LoginUserForm().as_p()}
            )
        del request.session['loggedUser']
        return HttpResponseRedirect('/')

    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            request.session['loggedUser'] = username
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.ERROR, _('Wrong password'))
                return HttpResponseRedirect(reverse('users:user-create'))

        messages.add_message(request, messages.ERROR, _('Form invalid'))
        return HttpResponseRedirect(reverse('users:user-create'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
