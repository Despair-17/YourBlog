from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

User = get_user_model()


class EmailAuthBackends(ModelBackend):
    def authenticate(
            self, request: HttpRequest, username: str = None, password: str = None, **kwargs: dict[str, Any]
    ) -> User | None:
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id: int) -> User | None:
        user_model = get_user_model()
        try:
            user = user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
