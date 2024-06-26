from datetime import datetime
from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm

from users.validators import EmailExistValidator


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        min_length=4,
        max_length=50,
        widget=forms.TextInput(),
        label=r'Логин / Email',
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
        validators=(
            EmailExistValidator(),
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


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
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'profile-image-select'}),
        }

    def __init__(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        user = kwargs.get('instance', None)
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self) -> str:
        email = self.cleaned_data['email']
        email_exist_validator = EmailExistValidator()
        email_exist_validator(email, self.user)
        return email


class PasswordChangeUserForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Старый пароль',
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Новый пароль',
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Повтор нового пароля',
    )
