from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from taggit.managers import TaggableManager

from django_ckeditor_5.fields import CKEditor5Field


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()

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
        upload_to='post_images/%Y/%m/%d/',
        blank=True,
        default=None,
        verbose_name='Изображение',
    )

    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
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

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-time_update',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})
