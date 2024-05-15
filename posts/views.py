from typing import Any

from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from unidecode import unidecode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView
from django.shortcuts import get_object_or_404
from django.db.models.functions import RowNumber
from django.db.models import F, Window, Count, QuerySet, Case, When, IntegerField

from taggit.models import Tag
from main.utils import DataMixin
from .forms import PostCreateForm

from .models import Post, Category
from .utils import PaginatedListView


class AllCategoriesView(DataMixin, TemplateView):
    template_name = 'posts/all_categories.html'
    title_page = 'Все категории'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        window = Window(
            expression=RowNumber(),
            partition_by=[F('category__name')],
            order_by=[F('time_update').desc()]
        )
        posts = Post.published.annotate(row_number=window).order_by('category__name')
        posts = posts.filter(row_number__lte=4).select_related('category')

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

    def get_queryset(self) -> QuerySet[Post]:
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        queryset = Post.published.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_context_mixin(context, title=self.category.name, category=self.category)


class PostsByTagsView(DataMixin, PaginatedListView):
    template_name = 'posts/posts_by_tag.html'
    context_object_name = 'posts_list'
    tag = None

    def get_queryset(self) -> QuerySet[Post]:
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        queryset = Post.published.filter(tags=self.tag).select_related('author', 'category')
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_context_mixin(context, title=self.tag.name, tag=self.tag)


class PostsSearchView(DataMixin, PaginatedListView):
    template_name = 'posts/search.html'
    context_object_name = 'posts_list'
    title_page = 'Результаты поиска'

    def get_queryset(self) -> QuerySet[Post]:
        search_query = self.request.GET.get('search_query')
        queryset = Post.published.filter(title__icontains=search_query)
        return queryset


class PostsExtendedSearchView(DataMixin, PaginatedListView):
    template_name = 'posts/extended_search.html'
    context_object_name = 'posts_list'
    title_page = 'Поиск'
    tags = None

    def get_queryset(self) -> QuerySet[Post] | list:
        category = self.request.GET.get('category')
        tags = self.request.GET.getlist('tags')

        if not category:
            return []

        queryset = Post.objects.filter(category=category)

        if tags:
            queryset = (Post.published
                        .filter(tags__id__in=tags)
                        .annotate(num_tags=Count('tags__id'))
                        .filter(num_tags=len(tags)))

        self.tags = Tag.objects.filter(taggit_taggeditem_items__object_id__in=queryset).distinct()
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        context['tags'] = self.tags
        return context


class MyPostsView(DataMixin, LoginRequiredMixin, CreateView):
    template_name = 'posts/my_posts.html'
    title_page = 'Мои посты'
    form_class = PostCreateForm
    success_url = reverse_lazy('my_posts')

    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.filter(author_id=self.request.user.pk)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        posts = self.get_queryset()

        context['published'] = [post for post in posts if post.is_published == Post.Status.PUBLISHED]
        context['draft'] = [post for post in posts if post.is_published == Post.Status.DRAFT]
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
