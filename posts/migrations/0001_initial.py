# Generated by Django 4.2.11 on 2024-05-04 21:37

from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=255, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Контент')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Слаг')),
                ('image', models.ImageField(blank=True, default=None, upload_to='post_images/%Y/%m/%d/', verbose_name='Изображение')),
                ('is_published', models.BooleanField(choices=[(True, 'Опубликовано'), (False, 'Черновик')], default=0, verbose_name='Статус')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ('-time_update',),
            },
        ),
    ]
