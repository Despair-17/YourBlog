from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from guardian.admin import GuardedModelAdmin

from .models import Category, Post


@admin.register(Post)
class PostAdmin(GuardedModelAdmin):
    list_display = ('title', 'post_image', 'author', 'category', 'slug', 'is_published', 'time_create',
                    'time_update')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 25
    fields = ('title', 'author', 'category', 'tags', 'content', 'slug', 'image', 'post_image', 'is_published')
    readonly_fields = ('post_image',)
    actions = ('set_published', 'set_draft')
    save_on_top = True

    @admin.display(description='Изображение')
    def post_image(self, post: Post) -> str:
        if post.image and post.image.url:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" alt="{}" height="50" width="50"></a>',
                post.image.url,
                post.image.url,
                post.title
            )
        return 'Нет картинки'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} записей.')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.update(is_published=Post.Status.DRAFT)
        self.message_user(request, f'Сняты {count} записей c публикации.')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
    fields = ('name', 'slug')
