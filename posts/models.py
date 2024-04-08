from django.contrib.auth import get_user_model
from django.db import models


class Posts(models.Model):
    class Status(models.IntegerChoices):
        PUBLISHED = (1, 'Опубликовано')
        DRAFT = (0, 'Черновик')

    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок',
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    category = models.ForeignKey(
        'Categories',
        on_delete=models.PROTECT,
        verbose_name='Категория',
    )

    content = models.TextField(
        blank=True,
        verbose_name='Контент'
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Слаг'
    )

    image = models.ImageField(
        upload_to='posts_images/%Y/%m/%d/',
        blank=True,
        default=None,
        verbose_name='Основная картинка поста',
    )

    is_published = models.BooleanField(
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус'
    )

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )

    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Время последнего изменения'
    )

    def __str__(self):
        return self.title


class Categories(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name='Слаг'
    )

    def __str__(self):
        return self.name
