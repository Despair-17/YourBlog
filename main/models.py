from django.db import models

from django_ckeditor_5.fields import CKEditor5Field


class Main(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название',
    )
    content = CKEditor5Field(
        blank=True,
        config_name='extends',
        verbose_name='Контент',
    )

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'

    def __str__(self) -> str:
        return f'{self.title}'


class About(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название',
    )
    content = CKEditor5Field(
        blank=True,
        config_name='extends',
        verbose_name='Контент',
    )

    class Meta:
        verbose_name = 'О сайте'
        verbose_name_plural = 'О сайте'

    def __str__(self) -> str:
        return f'{self.title}'


class FAQ(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название',
    )
    content = CKEditor5Field(
        blank=True,
        config_name='extends',
        verbose_name='Контент',
    )

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self) -> str:
        return f'{self.title}'
