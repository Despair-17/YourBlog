from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class EmailExistValidator:
    def __init__(self, message: str = None) -> None:
        self.message = message if message else 'Email уже занят.'

    def __call__(self, email: str, current_user: User = None) -> None:
        user_model = get_user_model()
        if current_user:
            if user_model.objects.filter(email=email).exclude(pk=current_user.pk).exists():
                raise ValidationError(self.message)
        else:
            if user_model.objects.filter(email=email).exists():
                raise ValidationError(self.message)
