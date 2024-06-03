import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PostContentStorage(FileSystemStorage):
    location = os.path.join(settings.MEDIA_ROOT, f'uploads/ckeditor/')
    base_url = urljoin(settings.MEDIA_URL, f'uploads/ckeditor/')
