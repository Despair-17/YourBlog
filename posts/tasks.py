from celery import shared_task
from celery.utils.log import get_task_logger

from main.utils import move_images

from .models import Post

logger = get_task_logger(__name__)


@shared_task
def move_image_to_permanent_location(post_id: int, filepath: str) -> None:
    post = Post.objects.get(pk=post_id)
    move_images(post, filepath, 'post_content')
