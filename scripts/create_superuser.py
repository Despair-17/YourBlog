import os
import sys

import django
from django.contrib.auth import get_user_model

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

from blog.settings.prod import DEBUG, env  # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'blog.settings.prod')

django.setup()

username = env.str('DJANGO_SUPERUSER_USERNAME')
email = env.str('DJANGO_SUPERUSER_EMAIL')
password = env.str('DJANGO_SUPERUSER_PASSWORD')

User = get_user_model()

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully')
else:
    print(f'Superuser {username} already exists')
