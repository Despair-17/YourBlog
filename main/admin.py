from django.contrib import admin

from .models import About, FAQ

admin.site.site_header = 'Администрирование YourBlog'


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ('title', 'content',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ('title', 'content',)
