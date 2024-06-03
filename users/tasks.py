from celery import shared_task
from celery.utils.log import get_task_logger

from django.contrib.auth import get_user_model

from main.utils import move_images

User = get_user_model()
logger = get_task_logger(__name__)


@shared_task
def move_image_to_permanent_location(user_id: int, filepath: str) -> None:
    user = User.objects.get(pk=user_id)
    move_images(user, filepath, 'users_content')
