from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from main.utils import DataMixin

from .forms import LoginUserForm, PasswordChangeUserForm, ProfileUserForm, RegisterUserForm
from .models import User


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


def register_user_done(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/register_done.html')


class ProfileUserView(DataMixin, LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    title_page = 'Профиль'
    model = get_user_model()
    form_class = ProfileUserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset: QuerySet | None = None) -> User:
        return self.request.user


class PasswordChangeUserView(DataMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    title_page = 'Изменение пароля'
    success_url = reverse_lazy('users:password_change_done')
    form_class = PasswordChangeUserForm
