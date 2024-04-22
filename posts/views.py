from django.views.generic import DetailView, TemplateView
from django.shortcuts import get_object_or_404
from django.db.models.functions import RowNumber
from django.db.models import F, Window

from taggit.models import Tag
from main.utils import DataMixin

from .models import Post, Category
from .utils import PaginatedListView


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

        context['posts_by_category'] = posts_by_category
        return context


class PostView(DataMixin, DetailView):
    template_name = 'posts/post.html'
    model = Post
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


class PostsByCategoryView(DataMixin, PaginatedListView):
    template_name = 'posts/posts_by_category.html'
    context_object_name = 'posts_list'
    category = None

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        queryset = Post.published.filter(category=self.category).select_related('author')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_context_mixin(context, title=self.category.name, category=self.category)


class PostsByTagsView(DataMixin, PaginatedListView):
    template_name = 'posts/posts_by_tag.html'
    context_object_name = 'posts_list'
    tag = None

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        queryset = Post.published.filter(tags=self.tag).select_related('author', 'category')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_context_mixin(context, title=self.tag.name, tag=self.tag)


class PostsSearchView(DataMixin, PaginatedListView):
    template_name = 'posts/search.html'
    context_object_name = 'posts_list'
    title_page = 'Результаты поиска'

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        queryset = Post.published.filter(title__icontains=search_query)
        return queryset


class PostsExtendedSearchView(DataMixin, PaginatedListView):
    template_name = 'posts/extended_search.html'
    context_object_name = 'posts_list'
    title_page = 'Поиск'

    def get_queryset(self):
        ...
