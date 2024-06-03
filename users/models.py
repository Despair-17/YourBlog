from typing import Any

from blog.settings.base import DEBUG

from django.contrib.auth.models import AbstractUser
from django.db import models

from main.utils import get_temp_upload_file


class User(AbstractUser):
    class Status(models.IntegerChoices):
        AUTHOR = (True, 'Автор статей')
        READER = (False, 'Читатель')

    is_author = models.BooleanField(
        choices=tuple((bool(x[0]), x[1]) for x in Status.choices),
        default=Status.READER,
        verbose_name='Автор статей'
    )

    date_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения',
    )

    image = models.ImageField(
        upload_to=get_temp_upload_file,
        blank=True,
        null=True,
        verbose_name='Фотография',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.username}'

    def save(self, *args: tuple[str], **kwargs: dict[str, Any]) -> None:
        super().save(*args, **kwargs)

        if self.image and self.image.url.startswith('/media/temp/'):
            from .tasks import move_image_to_permanent_location
            move_image_to_permanent_location.delay(self.pk, self.image.name)
