from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User as DjangoUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import AddUserForm, LoginUserForm
from .models import User


# Create your views here.


class AddUserView(View):
    """Register new user"""

    def get(self, request):
        form = AddUserForm().as_p()
        ctx = {'form': form}

        return render(request,
                      template_name='add_user.html',
                      context=ctx)

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            if DjangoUser.objects.filter(username=username).exists():
                return HttpResponseRedirect('/object_already_exist')

            django_user = DjangoUser.objects.create_user(username=username,
                                                         password=password,
                                                         first_name=first_name,
                                                         last_name=last_name,
                                                         email=email)
            User.objects.create(user=django_user)
            return HttpResponseRedirect('/users/users')
        return HttpResponseRedirect('/wrong_value')


class LoginUserView(View):
    """Login user"""

    def get(self, request):
        loggedUser = request.session.get('loggedUser')
        if loggedUser is None:
            form = LoginUserForm().as_p()
            ctx = {
                'form': form
            }
            return render(request,
                          template_name='login.html',
                          context=ctx)

        else:
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
                return HttpResponseRedirect('/wrong_password')
        else:
            return HttpResponseRedirect('/wrong_value')


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class ShowUsersView(View):
    def get(self, request):
        all_users = User.objects.all().order_by('user__username')

        ctx = {'all_users': all_users}

        return render(request,
                      template_name='users.html',
                      context=ctx)


class DeleteUserView(PermissionRequiredMixin, View):
    permission_required = 'game_recommendation.delete_genre'
    raise_exception = True

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponseRedirect('/users/users')
