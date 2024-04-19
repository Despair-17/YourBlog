from django.core.paginator import Page
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from django.db.models.functions import RowNumber
from django.db.models import F, Window

from .models import Post, Category
from taggit.models import Tag

from main.utils import DataMixin


class AllCategoriesView(DataMixin, TemplateView):
    template_name = 'posts/all_categories.html'
    title_page = 'Все категории'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        window = Window(
            expression=RowNumber(),
            partition_by=[F('category__name')],
            order_by=[F('time_update').desc()]
        )
        posts = Post.published.annotate(row_number=window).order_by('category__name')
        posts = posts.filter(row_number__lte=4).select_related('category', 'author')

        posts_by_category = {}
        for post in posts:
            posts_by_category.setdefault(post.category, []).append(post)

        context.update(
            {
                'posts_by_category': posts_by_category,
            }
        )
        return context


class PostView(DataMixin, DetailView):
    template_name = 'posts/post.html'
    model = Post
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


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


class PostsByTagsView(DataMixin, ListView):
    template_name = 'posts/posts_by_tag.html'
    model = Post
    context_object_name = 'posts_list'
    paginate_by = 8
    tag = None

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        posts_list = Post.published.filter(tags=self.tag).select_related('author', 'category')
        return posts_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page: Page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number)
        return self.get_context_mixin(context, title=self.tag.name, tag=self.tag)


class PostsSearchView(ListView):
    template_name = 'posts/search.html'
    model = Post
    context_object_name = 'posts_list'

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        posts_list = Post.published.filter(title__icontains=search_query)
        return posts_list
