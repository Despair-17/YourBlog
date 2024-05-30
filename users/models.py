from django.contrib.auth.models import AbstractUser
from django.db import models


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
        upload_to='users/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Фотография',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.username}'
