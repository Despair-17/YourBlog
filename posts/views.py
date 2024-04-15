from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from .models import Post, Category

from main.utils import DataMixin


class PostsByCategoryView(DataMixin, ListView):
    template_name = 'posts/posts_by_category.html'
    context_object_name = 'posts_list'
    paginate_by = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category = None

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        post_list = Post.published.filter(category=self.category)
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_context_mixin(context, title=self.category.name, category=self.category)
