from django.core.paginator import Page
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from .models import Post, Category

from main.utils import DataMixin


class PostsByCategoryView(DataMixin, ListView):
    template_name = 'posts/posts_by_category.html'
    context_object_name = 'posts_list'
    paginate_by = 8
    category = None

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        post_list = Post.published.filter(category=self.category).select_related('author')
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page: Page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number)
        return self.get_context_mixin(context, title=self.category.name, category=self.category)


class PostView(DataMixin, DetailView):
    template_name = 'posts/post.html'
    model = Post
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
