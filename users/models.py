from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Status(models.IntegerChoices):
        AUTHOR = (True, 'Автор статей')
        READER = (False, 'Читатель')

    is_author = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
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
