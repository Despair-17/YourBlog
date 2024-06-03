import os
import shutil
from typing import Any

from blog.settings.base import BASE_DIR, MEDIA_ROOT

from bs4 import BeautifulSoup

from celery.utils.log import get_task_logger

from django.db.models import Model

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'FAQ', 'url_name': 'faq'},
    {'title': 'Посты по категориям', 'url_name': 'all_categories'}
]


class DataMixin:
    title_page = None
    extra_context = {}

    def __init__(self) -> None:
        if self.title_page:
            self.extra_context['title'] = self.title_page

    @staticmethod
    def get_context_mixin(context: dict[str, Any], **kwargs: dict[str, Any]) -> dict[str, Any]:
        context.update(kwargs)
        return context


def get_temp_upload_file(instance: Model, filename: str) -> str:
    return os.path.join('temp/', filename)


def get_upload_file(instance: Model, filename: str, prefix: str) -> str:
    return os.path.join(f'{prefix}/{instance.pk}/', filename)


def extract_image_urls(html_content: str) -> list[str]:
    soup = BeautifulSoup(html_content, 'html.parser')
    image_urls = [img.get('src') for img in soup.find_all('img')]
    return image_urls


def get_full_media_path(url: str) -> str:
    if url.startswith('/'):
        url = url[1:]
    return os.path.join(BASE_DIR, url)


logger = get_task_logger(__name__)


def move_images(instance: Model, filepath: str, prefix: str) -> None:
    filename = os.path.basename(filepath)

    full_temp_path = os.path.join(MEDIA_ROOT, filepath)
    new_path = get_upload_file(instance, filename, prefix)
    full_perm_path = os.path.join(MEDIA_ROOT, new_path)

    try:
        os.makedirs(os.path.dirname(full_perm_path), exist_ok=True)
        shutil.move(full_temp_path, full_perm_path)

        instance.image = new_path
        instance.save()
    except PermissionError as err:
        logger.error(f'Failed to move file: {err}')
    except Exception as err:
        logger.error(f'An error occurred: {err}')
