from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.test import TestCase
from django.urls import reverse

from taggit.models import Tag

from .models import Category, Post


class TestAllCategoriesView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='password')

        self.category1 = Category.objects.create(name='Test 1', slug='test-1')
        self.category2 = Category.objects.create(name='Test 2', slug='test-2')

        self.count_published = 7
        self.count_draft = 3
        all_post_status = [True] * self.count_published + [False] * self.count_draft

        for cat in [self.category1, self.category2]:
            for i, status in enumerate(all_post_status):
                Post.objects.create(
                    title=f'Test {i}',
                    slug=f'test-{i}-{cat.slug}',
                    content='Test content',
                    category=cat,
                    is_published=status,
                    author=self.user1,
                )

        self.path = reverse('all_categories')

    def test_view_renders_correct_template(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/all_categories.html')

    def test_view_context(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Все категории')
        self.assertContains(response, 'Test 1')
        self.assertContains(response, 'Test 2')

        posts_by_category = response.context['posts_by_category']

        self.assertEquals(len(posts_by_category), 2)
        self.assertEquals(len(posts_by_category[self.category1]), 4)
        self.assertEquals(len(posts_by_category[self.category2]), 4)

    def test_correct_posts_selected(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)

        posts_by_category = response.context['posts_by_category']

        posts_category1 = Post.objects.filter(category=self.category1, is_published=True).order_by('-time_update')[:4]
        posts_category2 = Post.objects.filter(category=self.category2, is_published=True).order_by('-time_update')[:4]

        self.assertEquals(posts_by_category[self.category1], list(posts_category1))
        self.assertEquals(posts_by_category[self.category2], list(posts_category2))


class TestPostsByCategoryView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='password')

        self.category1 = Category.objects.create(name='Test 1', slug='test-1')

        self.count_published = 20
        self.count_draft = 3
        all_post_status = [True] * self.count_published + [False] * self.count_draft

        for i, status in enumerate(all_post_status):
            Post.objects.create(
                title=f'Test {i}',
                slug=f'test-{i}-{self.category1.slug}',
                content='Test content',
                category=self.category1,
                is_published=status,
                author=self.user1,
            )

        self.path = reverse('category', args=(self.category1.slug,))

    def test_view_render_correct_template(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/posts_by_category.html')

    def test_view_context(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context['category'], self.category1)
        self.assertEquals(response.context['title'], self.category1.name)

    def test_view_queryset(self):
        response = self.client.get(self.path)

        post_list = response.context['posts_list']
        posts = Post.published.filter(category=self.category1)

        self.assertEquals(len(post_list), 8)
        self.assertQuerysetEqual(post_list, posts[:8])

    def test_view_paginate(self):
        page_number = 3
        page_size = 8
        response = self.client.get(self.path, {'page': page_number})

        self.assertEquals(response.status_code, HTTPStatus.OK)

        post_list = response.context['posts_list']
        posts = Post.published.filter(category=self.category1).order_by('-time_update')

        self.assertQuerysetEqual(post_list, posts[page_size * (page_number - 1):page_size * page_number])


class TestPostsByTagsView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='password')

        self.category1 = Category.objects.create(name='Test 1', slug='test-1')
        self.tag1 = Tag.objects.create(name='Тег 1', slug='tag-1')

        self.count_published = 7
        self.count_draft = 3
        all_post_status = [True] * self.count_published + [False] * self.count_draft

        for i, status in enumerate(all_post_status):
            post = Post.objects.create(
                title=f'Test {i}',
                slug=f'test-{i}-{self.category1.slug}',
                content='Test content',
                category=self.category1,
                is_published=status,
                author=self.user1,
            )
            post.tags.add(self.tag1)

        self.path = reverse('tag', args=(self.tag1.slug,))

    def test_view_render_correct_template(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/posts_by_tag.html')

    def test_view_context(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context['tag'], self.tag1)
        self.assertEquals(response.context['title'], self.tag1.name)

    #
    def test_view_queryset(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)

        post_list = response.context['posts_list']
        posts = Post.published.filter(tags=self.tag1)

        self.assertEquals(len(post_list), 7)
        self.assertQuerysetEqual(post_list, posts[:7])

    #
    def test_view_paginate(self):
        page_number = 1
        page_size = 8
        response = self.client.get(self.path, {'page': page_number})

        self.assertEquals(response.status_code, HTTPStatus.OK)

        post_list = response.context['posts_list']
        posts = Post.published.filter(tags=self.tag1).order_by('-time_update')
        self.assertQuerysetEqual(post_list, posts[page_size * (page_number - 1):page_size * page_number])


class TestPostsSearchView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='password')

        self.category1 = Category.objects.create(name='Test 1', slug='test-1')

        self.count_published = 20
        self.count_draft = 3
        all_post_status = [True] * self.count_published + [False] * self.count_draft

        for i, status in enumerate(all_post_status):
            Post.objects.create(
                title=f'Test {i}',
                slug=f'test-{i}-{self.category1.slug}',
                content='Test content',
                category=self.category1,
                is_published=status,
                author=self.user1,
            )

        self.path = reverse('search')

    def test_view_render_correct_template(self):
        response = self.client.get(self.path, {'search_query': 'test title 2'})

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/search.html')

    def test_view_context(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context['title'], 'Результаты поиска')

    def test_view_queryset(self):
        response = self.client.get(self.path, {'search_query': 'Test 1'})

        self.assertEquals(response.status_code, HTTPStatus.OK)

        post_list = response.context['posts_list']
        posts = Post.published.filter(title__icontains='Test 1')

        self.assertEquals(len(post_list), 8)
        self.assertQuerysetEqual(post_list, posts[:8])

    def test_view_paginate(self):
        page_number = 2
        page_size = 8
        response = self.client.get(self.path, {'search_query': 'Test 1', 'page': page_number})

        self.assertEquals(response.status_code, HTTPStatus.OK)

        post_list = response.context['posts_list']
        posts = Post.published.filter(title__icontains='Test 1')

        self.assertQuerysetEqual(post_list, posts[page_size * (page_number - 1):page_size * page_number])


class TestPostsExtendedSearchView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='password')

        self.category1 = Category.objects.create(name='Test 1', slug='test-1')
        self.tags = [Tag.objects.create(name=f'Тег {i}', slug=f'tag-{i}') for i in range(3)]

        self.count_published = 20
        self.count_draft = 3
        all_post_status = [True] * self.count_published + [False] * self.count_draft

        for i, status in enumerate(all_post_status):
            post = Post.objects.create(
                title=f'Test {i}',
                slug=f'test-{i}-{self.category1.slug}',
                content='Test content',
                category=self.category1,
                is_published=status,
                author=self.user1,
            )
            post.tags.set(self.tags)

        self.path = reverse('extended_search')

    def test_view_render_correct_template(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/search_extended.html')

    def test_view_context(self):
        response = self.client.get(self.path, {'category': self.category1.pk})

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context['title'], 'Поиск')

        categories = Category.objects.all()

        self.assertQuerysetEqual(response.context['categories'], categories)

        posts = Post.published.filter(category=self.category1)
        tags = Tag.objects.filter(taggit_taggeditem_items__object_id__in=posts).distinct()

        self.assertQuerysetEqual(list(response.context['tags']), list(tags))

    def test_view_queryset(self):
        response = self.client.get(
            self.path,
            {'category': self.category1.pk, 'tags': [self.tags[0].pk, self.tags[2].pk]}
        )

        self.assertEquals(response.status_code, HTTPStatus.OK)

        post_list = response.context['posts_list']

        self.assertEquals(len(post_list), 8)

        posts = (Post.published
                 .filter(category=self.category1)
                 .filter(tags__id__in=[self.tags[0].pk, self.tags[2].pk])
                 .annotate(num_tags=Count('tags'))
                 .filter(num_tags=2)
                 .order_by('-time_update')[:8])

        self.assertQuerysetEqual(post_list, posts)

    def test_view_paginate(self):
        page_number = 1
        page_size = 8
        response = self.client.get(
            self.path,
            {'category': self.category1.pk, 'tags': [self.tags[0].pk, self.tags[2].pk]}
        )

        self.assertEquals(response.status_code, HTTPStatus.OK)

        post_list = response.context['posts_list']
        posts = (Post.published
                 .filter(category=self.category1)
                 .filter(tags__id__in=[self.tags[0].pk, self.tags[2].pk])
                 .annotate(num_tags=Count('tags'))
                 .filter(num_tags=2)
                 .order_by('-time_update')[:8])

        self.assertQuerysetEqual(post_list, posts[page_size * (page_number - 1):page_size * page_number])


class TesttPostDetailView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.author = self.user_model.objects.create_user(username='author', password='password')
        self.another_user = self.user_model.objects.create_user(username='another_user', password='password')

        self.category1 = Category.objects.create(name='Test 1', slug='test-1')
        self.tags = [Tag.objects.create(name=f'Тег {i}', slug=f'tag-{i}') for i in range(3)]

        self.post = Post.objects.create(
            title=f'Test 1',
            slug=f'test-1',
            content='Test content',
            category=self.category1,
            is_published=True,
            author=self.author,
        )
        self.post.tags.set(self.tags)

        self.path = reverse('post', args=(self.post.slug,))

    def test_view_renders_correct_template(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_view_returns_correct_post(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['post'], self.post)

    def test_view_context_for_anonymous_user(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('permitted_items', response.context)
        self.assertEquals(response.context['permitted_items'], [])

    def test_view_context_for_another_user(self):
        self.client.login(username='another_user', password='password')

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('permitted_items', response.context)
        self.assertEquals(response.context['permitted_items'], [])

        self.post.is_published = False
        self.post.save()
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)

    def test_view_context_for_author(self):
        self.client.login(username='author', password='password')

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('permitted_items', response.context)
        self.assertIn('change_post', response.context['permitted_items'])
        self.assertIn('delete_post', response.context['permitted_items'])


class TestMyPostsCreateView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='password')

        self.category1 = Category.objects.create(name='Test 1', slug='test-1')
        self.tags = 'Tag 1, Tag2, Tag3'

        self.count_published = 7
        self.count_draft = 3
        all_post_status = [True] * self.count_published + [False] * self.count_draft

        for i, status in enumerate(all_post_status):
            Post.objects.create(
                title=f'Test {i}',
                slug=f'test-{i}-{self.category1.slug}',
                content='Test content',
                category=self.category1,
                is_published=status,
                author=self.user1,
            )

        self.path = reverse('my_posts')

    def test_view_renders_correct_template_anonymous(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f'/users/accounts/login/?next={self.path}')

    def test_view_renders_correct_template_login_user(self):
        self.client.login(username='user1', password='password')

        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/posts_user.html')
        self.assertContains(response, 'Мои посты')

    def test_view_context_correct(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertIn('draft', response.context)
        self.assertIn('published', response.context)

        draft = Post.objects.filter(is_published=Post.Status.DRAFT, author=self.user1)
        published = Post.objects.filter(is_published=Post.Status.PUBLISHED, author=self.user1)

        self.assertQuerysetEqual(response.context['draft'], draft)
        self.assertQuerysetEqual(response.context['published'], published)

    def test_form_processing_valid(self):
        self.client.login(username='user1', password='password')

        slug = f'test-{self.count_draft + self.count_published + 1}'

        form_data = {
            'title': 'Test',
            'slug': slug,
            'content': 'Test content',
            'category': self.category1.pk,
            'tags': self.tags,
            'image': '',
            'is_published': True,
        }

        response = self.client.post(self.path, form_data)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        new_post = Post.published.get(slug=slug)

        self.assertEquals(new_post.author, self.user1)
        self.assertEquals(new_post.is_published, True)
        self.assertEquals(new_post.category, self.category1)

        post_tags = Tag.objects.filter(taggit_taggeditem_items__object_id=new_post.id).order_by('name')

        self.assertQuerysetEqual(post_tags, self.tags.split(', '), transform=lambda x: x.name)

    def test_form_processing_invalid(self):
        self.client.login(username='user1', password='password')

        form_data = {
            'title': '',
            'slug': '',
            'content': '',
            'category': '',
            'tags': '',
            'image': '',
            'is_published': '',
        }
        response = self.client.post(self.path, form_data)

        self.assertEquals(response.status_code, HTTPStatus.OK)

        self.assertFormError(
            response,
            'form',
            'title',
            'Это поле обязательно для заполнения.'
        )

        self.assertFormError(
            response,
            'form',
            'slug',
            'Это поле обязательно для заполнения.'
        )

        self.assertFormError(
            response,
            'form',
            'category',
            'Это поле обязательно для заполнения.'
        )

        self.assertFormError(
            response,
            'form',
            'is_published',
            'Это поле обязательно для заполнения.'
        )

        form_data = {
            'title': 'invalid!@#$%^&',
            'slug': f'test-1-{self.category1.slug}',
            'content': '',
            'category': 'invalid',
            'tags': '',
            'image': '',
            'is_published': 'invalid',
        }
        response = self.client.post(self.path, form_data)

        self.assertEquals(response.status_code, HTTPStatus.OK)

        self.assertFormError(
            response,
            'form',
            'slug',
            'Пост с таким Слаг уже существует.'
        )

        self.assertFormError(
            response,
            'form',
            'category',
            'Выберите корректный вариант. Вашего варианта нет среди допустимых значений.'
        )

        self.assertFormError(
            response,
            'form',
            'is_published',
            'Выберите корректный вариант. invalid нет среди допустимых значений.'
        )


class TestMyPostsUpdateView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='password')

        self.category1 = Category.objects.create(name='Test 1', slug='test-1')

        self.post = Post.objects.create(
            title=f'Test 1',
            slug=f'test-1',
            content='Test content',
            category=self.category1,
            is_published=True,
            author=self.user1,
        )

        self.path = reverse('update_post', args=(self.post.slug,))

    def test_view_renders_correct_template_anonymous(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f'/users/accounts/login/?next={self.path}')

    def test_view_renders_correct_template_login_user(self):
        self.client.login(username='user1', password='password')

        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/post_update.html')
        self.assertContains(response, 'Обновление поста')


class TestMyPostsDeleteView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='password')

        self.category1 = Category.objects.create(name='Test 1', slug='test-1')

        self.post = Post.objects.create(
            title=f'Test 1',
            slug=f'test-1',
            content='Test content',
            category=self.category1,
            is_published=True,
            author=self.user1,
        )
        self.path = reverse('delete_post', args=(self.post.slug,))

    def test_view_renders_correct_template_anonymous(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f'/users/accounts/login/?next={self.path}')

    def test_view_renders_correct_template_login_user(self):
        self.client.login(username='user1', password='password')

        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/post_delete.html')
        self.assertContains(response, 'Удаление поста')
