from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from main.utils import DataMixin
from .form import LoginUserForm, RegisterUserForm


class LoginUserView(DataMixin, LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginUserForm
    title_page = 'Войти'


class RegisterUserView(DataMixin, CreateView):
    template_name = 'users/register.html'
    model = get_user_model()
    form_class = RegisterUserForm
    title_page = 'Регистрация'
    success_url = reverse_lazy('users:register_done')


class RegisterUserDoneView(DataMixin, TemplateView):
    template_name = 'users/register_done.html'
    title_page = 'Успешная регистрация'
