from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.core.exceptions import ValidationError

from django import forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        min_length=4,
        max_length=50,
        widget=forms.TextInput(),
        label='Логин',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Пароль',
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self) -> str:
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Email уже занят.')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        required=True,
        label='Логин'
    )

    email = forms.EmailField(
        required=True,
        label='Email',
    )

    this_year = datetime.now().year
    date_birth = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(
            years=tuple(range(this_year - 100, this_year - 17)),
            empty_label=('Год', 'Месяц', 'День'),
        ),
        label='Дата рождения',
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'date_birth', 'image')
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'image': 'Фотография'}