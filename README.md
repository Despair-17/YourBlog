# Blog

В процессе разработки...

## Требования

- Python 3.8+
- pip
- Docker (для Docker-версии)

## Установка и запуск

### Dev версия (без Docker, с SQLite, c debug_toolbar и без кэширования для отладки)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Despair-17/YourBlog.git
   cd YourBlog
   ```
2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   venv\Scripts\activate.bat на Windows
   
   python3 -m venv venv
   source venv/bin/activate на Linux
   ```
3. Установите зависимости
   ```bash
   pip install -r requirements/dev.txt
   ```
4. Выполните миграции и запустите сервер:
   ```bash
   python manage.py makemigrations --settings=blog.settings.dev
   python manage.py migrate --settings=blog.settings.dev
   python manage.py runserver --settings=blog.settings.dev 0.0.0.0:8000
   ```
   
### Prod версия (без Docker, с PostgreSQL и Redis)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Despair-17/YourBlog.git
   cd YourBlog
   ```
2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   venv\Scripts\activate.bat на Windows
   
   python3 -m venv venv
   source venv/bin/activate на Linux
   ```
3. Установите зависимости
   ```bash
   pip install -r requirements/prod.txt
   ```
4. Выполните миграции и соберите статику:
   ```bash
   python manage.py makemigrations --settings=blog.settings.dev
   python manage.py migrate --settings=blog.settings.dev
   python manage.py collectstatic
   ```
5. Запустите сервер (например, с Gunicorn):
   ```bash
   gunicorn blog.wsgi:application --env DJANGO_SETTINGS_MODULE=blog.settings.prod --bind 0.0.0.0:8000
   ```

### Версия с Docker
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Despair-17/YourBlog.git
   cd YourBlog
   ```
2. Запустите контейнеры Docker:
   ```bash
   docker-compose up --build
   ```
3. Приложение будет доступно по адресу:
   ```bash
   http://localhost
   ```

### Дополнительная информация
Необходимо создать файл .env с переменными окружения в корне проекта, пример такого файла находится в корне
.env.template

### Пояснение

1. **Требования**: Перечислены все необходимые зависимости.
2. **Установка**:
   - Dev версия без Docker, с SQLite, c debug_toolbar и без кэширования для отладки.
   - Prod версия без Docker, использующая PostgreSQL и Redis.
   - Версия с Docker, которая включает использование Nginx, Gunicorn, PostgreSQL и Redis.
3. **Дополнительная информация**:
   - .env файл.