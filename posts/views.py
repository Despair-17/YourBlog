from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.db.models.functions import RowNumber
from django.db.models import F, Window, Count, QuerySet
from django.core.cache import cache

from guardian.shortcuts import get_perms
from guardian.mixins import PermissionListMixin
from taggit.models import Tag
from main.utils import DataMixin

from .forms import MyPostForm
from .models import Post, Category
from .utils import PaginatedListView
from blog.settings.base import CACHE_TTL_FCH


class AllCategoriesView(DataMixin, TemplateView):
    template_name = 'posts/all_categories.html'
    title_page = 'Все категории'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        cache_key = 'all_categories'
        posts_by_category = cache.get(cache_key)

        if not posts_by_category:
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

            cache.set(cache_key, posts_by_category, CACHE_TTL_FCH)

        context['posts_by_category'] = posts_by_category

        return context


class PostsByCategoryView(DataMixin, PaginatedListView):
    template_name = 'posts/posts_by_category.html'
    context_object_name = 'posts_list'
    category = None

    def get_queryset(self) -> QuerySet[Post]:
        cache_key_cats = f'posts_by_category_cat_{self.kwargs["category_slug"]}'
        cache_key_posts = f'posts_by_category_posts_{self.kwargs["category_slug"]}'

        self.category = cache.get(cache_key_cats)
        posts = cache.get(cache_key_posts)

        if not self.category:
            self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
            cache.set(cache_key_cats, self.category, CACHE_TTL_FCH)

        if not posts:
            posts = Post.published.filter(category=self.category)
            cache.set(cache_key_posts, posts, CACHE_TTL_FCH)

        return posts

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_context_mixin(context, title=self.category.name, category=self.category)


class PostsByTagsView(DataMixin, PaginatedListView):
    template_name = 'posts/posts_by_tag.html'
    context_object_name = 'posts_list'
    tag = None

    def get_queryset(self) -> QuerySet[Post]:
        cache_key_tag = f'posts_by_tags_tag_{self.kwargs["tag_slug"]}'
        cache_key_posts = f'posts_by_tags_posts_{self.kwargs["tag_slug"]}'

        self.tag = cache.get(cache_key_tag)
        posts = cache.get(cache_key_posts)

        if not self.tag:
            self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            cache.set(cache_key_tag, self.tag, CACHE_TTL_FCH)

        if not posts:
            posts = Post.published.filter(tags=self.tag).select_related('author', 'category')
            cache.set(cache_key_posts, posts, CACHE_TTL_FCH)

        return posts

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_context_mixin(context, title=self.tag.name, tag=self.tag)


class PostsSearchView(DataMixin, PaginatedListView):
    template_name = 'posts/search.html'
    context_object_name = 'posts_list'
    title_page = 'Результаты поиска'

    def get_queryset(self) -> QuerySet[Post]:
        search_query = self.request.GET.get('search_query', '')

        cache_search_query = '_'.join(search_query.split())
        cache_key = f'posts_search_{cache_search_query}'

        posts = cache.get(cache_key)

        if not posts:
            posts = Post.published.filter(title__icontains=search_query).order_by('-time_update')
            cache.set(cache_key, posts, CACHE_TTL_FCH)

        return posts


class PostsExtendedSearchView(DataMixin, PaginatedListView):
    template_name = 'posts/search_extended.html'
    context_object_name = 'posts_list'
    title_page = 'Поиск'
    tags = None

    def get_queryset(self) -> QuerySet[Post] | list:
        category = self.request.GET.get('category')
        tags = self.request.GET.getlist('tags')

        tags_str = ','.join(tags)
        cache_key_posts = f'posts_extended_search_posts_{category}_{tags_str}'
        cache_key_tags = f'posts_extended_search_tags_{category}_{tags_str}'

        posts = cache.get(cache_key_posts)
        self.tags = cache.get(cache_key_tags)

        if not category:
            return []

        if not posts:
            posts = Post.published.filter(category=category)

            if tags:
                posts = (Post.published
                         .filter(tags__id__in=tags)
                         .annotate(num_tags=Count('tags__id'))
                         .filter(num_tags=len(tags)))

            posts = posts.order_by('-time_update')
            cache.set(cache_key_posts, posts, CACHE_TTL_FCH)

            if not self.tags:
                self.tags = Tag.objects.filter(taggit_taggeditem_items__object_id__in=posts).distinct()
                cache.set(cache_key_tags, self.tags, CACHE_TTL_FCH)

        return posts

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache_key = f'posts_extended_search_category'

        categories = cache.get(cache_key)

        if not categories:
            categories = Category.objects.all()
            cache.set(cache_key, categories, CACHE_TTL_FCH)

        context['categories'] = categories
        context['tags'] = self.tags
        return context


class PostDetailView(DataMixin, DetailView):
    template_name = 'posts/post_detail.html'
    model = Post
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        cache_key = f'post_detail_{self.kwargs[self.slug_url_kwarg]}'

        post_obj = cache.get(cache_key)

        if not post_obj:
            posts = self.model.objects.filter(slug=self.kwargs[self.slug_url_kwarg])
            posts = posts.select_related('category', 'author').prefetch_related('tags')

            post_obj = get_object_or_404(posts, slug=self.kwargs[self.slug_url_kwarg])

            cache.set(cache_key, post_obj, CACHE_TTL_FCH)

        if not post_obj.is_published and ('change_post' not in get_perms(self.request.user, post_obj)):
            raise Http404

        return post_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_key = f'post_detail_{self.kwargs[self.slug_url_kwarg]}_{self.request.user.pk}'

        permitted_items = cache.get(cache_key)

        if not permitted_items:
            post = self.object
            user = self.request.user
            permitted_items = get_perms(user, post)
            cache.set(cache_key, permitted_items, CACHE_TTL_FCH)

        context['permitted_items'] = permitted_items

        return context


class MyPostsCreateView(DataMixin, LoginRequiredMixin, CreateView):
    template_name = 'posts/posts_user.html'
    title_page = 'Мои посты'
    form_class = MyPostForm
    success_url = reverse_lazy('my_posts')

    def get_queryset(self) -> QuerySet[Post]:
        posts = Post.objects.filter(author_id=self.request.user.pk)
        return posts

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache_key = f'my_posts_create_{self.request.user.pk}'

        post_list = cache.get(cache_key)

        if not post_list:
            posts = self.get_queryset()
            posts_published = [post for post in posts if post.is_published == Post.Status.PUBLISHED]
            posts_draft = [post for post in posts if post.is_published == Post.Status.DRAFT]
            cache.set(cache_key, [posts_published, posts_draft], CACHE_TTL_FCH)
        else:
            posts_published, posts_draft = post_list

        context['published'] = posts_published
        context['draft'] = posts_draft

        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MyPostsUpdateView(DataMixin, LoginRequiredMixin, PermissionListMixin, UpdateView):
    template_name = 'posts/post_update.html'
    title_page = 'Обновление поста'
    form_class = MyPostForm
    slug_url_kwarg = 'post_slug'
    model = Post
    permission_required = 'change_post'

    def get_object(self, queryset=None):
        cache_key = f'my_posts_update_{self.kwargs[self.slug_url_kwarg]}_{self.request.user.pk}'

        post_obj = cache.get(cache_key)

        if not post_obj:
            posts = self.model.objects.filter(slug=self.kwargs[self.slug_url_kwarg])
            posts = posts.select_related('category', 'author')

            post_obj = get_object_or_404(posts, slug=self.kwargs[self.slug_url_kwarg])

            cache.set(cache_key, post_obj, CACHE_TTL_FCH)

        return post_obj

    def get_success_url(self):
        return reverse_lazy('post', kwargs={self.slug_url_kwarg: self.kwargs[self.slug_url_kwarg]})


class MyPostsDeleteView(DataMixin, LoginRequiredMixin, PermissionListMixin, DeleteView):
    template_name = 'posts/post_delete.html'
    title_page = 'Удаление поста'
    model = Post
    slug_url_kwarg = 'post_slug'
    permission_required = 'delete_post'
    success_url = reverse_lazy('my_posts')
