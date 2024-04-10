# Generated by Django 4.2.11 on 2024-04-08 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=255, verbose_name='Слаг')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Слаг')),
                ('images', models.ImageField(blank=True, default=None, upload_to='posts_images/%Y/%m/%d/', verbose_name='Основная картинка поста')),
                ('is_published', models.BooleanField(choices=[(1, 'Опубликовано'), (0, 'Черновик')], default=0, verbose_name='Статус')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='posts.categories', verbose_name='Категория')),
            ],
        ),
    ]
