import os
from itertools import chain

from blog.settings.base import CONTACT_EMAIL, DEFAULT_FROM_EMAIL
from blog.settings.base import MEDIA_ROOT

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.files.storage import default_storage
from django.core.mail import send_mail

from main.models import About, FAQ, Main

from posts.models import Post

from .utils import extract_image_urls, get_full_media_path

logger = get_task_logger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def send_feedback_email(self, name: str, email: str, message: str) -> None:  # noqa: ANN001
    try:
        send_mail(
            subject='Новое сообщение обратной связи',
            message=f'Имя: {name}\nEmail: {email}\nСообщение: {message}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[CONTACT_EMAIL],
        )
        logger.info('Feedback email sent successfully.')

    except Exception as err:
        logger.error(f'Failed to send feedback email: {err}')
        self.retry(exp=err)


@shared_task
def remove_unused_files_ckeditor() -> None:
    ckeditor_upload_path = os.path.join(MEDIA_ROOT, 'uploads/ckeditor/')

    all_files = set()
    for dirname, _, filenames in os.walk(ckeditor_upload_path):
        for filename in filenames:
            full_path_file = os.path.join(dirname, filename)
            all_files.add(full_path_file)

    content_main = Main.objects.all().values('content')
    content_about = About.objects.all().values('content')
    content_faq = FAQ.objects.all().values('content')

    content_menu = content_main.union(content_about, content_faq)
    contents_post = Post.objects.all().values('content')

    used_files = set()
    for html_content in chain(content_menu, contents_post):
        if html_content['content']:
            full_path_images = (get_full_media_path(img_url) for img_url in extract_image_urls(html_content['content']))
            used_files.update(full_path_images)

    unused_files = all_files.difference(used_files)

    for path_file in unused_files:
        if default_storage.exists(path_file):
            default_storage.delete(path_file)
