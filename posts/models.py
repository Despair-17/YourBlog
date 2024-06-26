from typing import Any

from blog.settings.base import DEBUG

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse

from django_ckeditor_5.fields import CKEditor5Field

from guardian.shortcuts import assign_perm

from main.utils import get_temp_upload_file

from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet['Post']:
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.IntegerChoices):
        PUBLISHED = (True, 'Опубликовано')
        DRAFT = (False, 'Черновик')

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
        'Category',
        on_delete=models.PROTECT,
        verbose_name='Категория',
    )

    content = CKEditor5Field(
        blank=True,
        config_name='extends',
        verbose_name='Контент',
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Слаг'
    )

    image = models.ImageField(
        upload_to=get_temp_upload_file,
        blank=True,
        default=None,
        verbose_name='Изображение',
    )

    is_published = models.BooleanField(
        choices=tuple((bool(x[0]), x[1]) for x in Status.choices),
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

    tags = TaggableManager(
        blank=True,
        verbose_name='Теги',
        related_name='posts',
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-time_update',)

    def __str__(self) -> str:
        return self.title

    def save(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        super().save(*args, **kwargs)
        assign_perm('change_post', self.author, self)
        assign_perm('delete_post', self.author, self)

        if self.image and self.image.url.startswith('/media/temp/'):
            from .tasks import move_image_to_permanent_location
            move_image_to_permanent_location.delay(self.pk, self.image.name)

    def get_absolute_url(self) -> str:
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('category', kwargs={'category_slug': self.slug})
