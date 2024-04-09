from django.contrib import admin
from .models import Posts
from .models import Categories


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'author', 'category', 'slug', 'is_published')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_per_page = 10
    fields = ('title', 'author', 'category', 'content', 'slug', 'image', 'is_published')
    save_on_top = True


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    list_per_page = 10
    fields = ('name', 'slug')
