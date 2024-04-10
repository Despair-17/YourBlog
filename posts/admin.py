from django.contrib import admin

from django.utils.safestring import mark_safe

from .models import Post
from .models import Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_image', 'author', 'category', 'slug', 'is_published')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10
    fields = ('title', 'author', 'category', 'content', 'slug', 'image', 'post_image', 'is_published')
    readonly_fields = ('post_image',)
    save_on_top = True

    @admin.display(description='Изображение')
    def post_image(self, post: Post):
        if post.image.url:
            return mark_safe(f'<a href="{post.image.url}">'
                             f'<img src="{post.image.url}" alt="{post.title}" height=50 width=50></a>')
        return 'Нет картинки'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
    fields = ('name', 'slug')
