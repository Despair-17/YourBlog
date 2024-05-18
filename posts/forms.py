from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from taggit.forms import TagWidget

from posts.models import Post


class MyPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'content', 'category', 'tags', 'image', 'is_published')
        widgets = {
            'content': CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name='extends'),
            'tags': TagWidget(attrs={'placeholder': 'Список тегов через запятую.'})
        }
