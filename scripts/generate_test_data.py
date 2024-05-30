import os

from blog.settings.prod import BASE_DIR

from django.contrib.auth import get_user_model

from posts.models import Category, Post

content = """Это тестовый пост для проверки пагинации постов
Это тестовый пост для проверки пагинации постов
Это тестовый пост для проверки пагинации постов
Это тестовый пост для проверки пагинации постов
Это тестовый пост для проверки пагинации постов
Это тестовый пост для проверки пагинации постов"""


def generate_test_data(count: int) -> None:
    """Скрип для создания тестовый записей в модель Post.

    Запускать через python manage.py runscript generate_test_data
    """
    user = get_user_model().objects.get(username='root')

    category = Category.objects.get(name='Test')

    for i in range(1, count + 1):
        post = Post.objects.create(
            title=f'Test title {i}',
            author=user,
            category=category,
            content=content,
            slug=f'test-{i}',
            is_published=True,
        )
        image_path = os.path.join(BASE_DIR, 'media', 'post_images', 'default_image.png')
        with open(image_path, 'rb') as file:
            post.image.save('default_images.png', file, save=True)


def run() -> None:
    generate_test_data(50)
