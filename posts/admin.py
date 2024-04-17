from django.contrib import admin

from django.utils.safestring import mark_safe

from .models import Post
from .models import Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_image', 'author', 'category', 'slug', 'is_published', 'time_create', 'time_update')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 25
    fields = ('title', 'author', 'category', 'content', 'slug', 'image', 'post_image', 'is_published')
    readonly_fields = ('post_image',)
    actions = ('set_published', 'set_draft')
    save_on_top = True

    @admin.display(description='Изображение')
    def post_image(self, post: Post):
        if post.image.url:
            return mark_safe(f'<a href="{post.image.url}" target="_blank">'
                             f'<img src="{post.image.url}" alt="{post.title}" height=50 width=50></a>')
        return 'Нет картинки'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} записей.')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
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
