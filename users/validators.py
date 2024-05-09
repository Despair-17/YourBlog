from django.contrib.auth import get_user_model
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class EmailExistValidator:
    def __init__(self, message: str = None):
        self.massage = message if message else 'Email уже занят.'

    def __call__(self, email, *args, **kwargs):
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(self.massage)
