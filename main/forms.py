from captcha.fields import CaptchaField

from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        min_length=4,
        max_length=255,
        required=True,
        label='Имя'
    )

    email = forms.EmailField(
        required=True,
        label='Email',
    )

    message = forms.CharField(
        min_length=50,
        widget=forms.Textarea(),
        label='Сообщение',
    )

    captcha = CaptchaField()
