from django.db import models


class About(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='О сайте')

    class Meta:
        verbose_name = 'О сайте'
        verbose_name_plural = 'О сайте'


class FAQ(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Вопросы')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
