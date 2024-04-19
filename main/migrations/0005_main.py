# Generated by Django 4.2.11 on 2024-04-19 17:42

from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_about_content_alter_faq_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Контент')),
            ],
        ),
    ]
