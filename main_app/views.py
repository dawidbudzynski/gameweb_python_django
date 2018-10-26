from django.views.generic import TemplateView


# Create your views here.

class AboutPageView(TemplateView):
    template_name = 'about.html'


class WrongValueView(TemplateView):
    template_name = 'wrong_value_error.html'


class ObjectAlreadyExistView(TemplateView):
    template_name = 'object_already_exist.html'


class WrongPasswordView(TemplateView):
    template_name = 'wrong_password.html'
