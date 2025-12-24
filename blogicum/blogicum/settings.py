from pathlib import Path

# Определяет корневую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ для криптографических операций Django
SECRET_KEY = 'django-insecure-#r1f99e6(r8yo1g-n3j^99(ryy)x3z0th2s)6u@r)a*j@t_j0%'

# Режим отладки - включает подробные сообщения об ошибках
DEBUG = True

# Список разрешенных хостов для доступа к приложению
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# IP-адреса для доступа к debug_toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# Установленные приложения
INSTALLED_APPS = [
    # Стандартные Django-приложения
    'django.contrib.admin',  # Административная панель
    'django.contrib.auth',  # Система аутентификации
    'django.contrib.contenttypes',  # Типы контента
    'django.contrib.sessions',  # Сессии
    'django.contrib.messages',  # Система сообщений
    'django.contrib.staticfiles',  # Статические файлы

    # Внешние библиотеки
    'django_bootstrap5',  # Bootstrap 5 для Django
    'debug_toolbar',  # Инструменты отладки

    # Собственные приложения
    'pages.apps.PagesConfig',  # Приложение pages
    'blog.apps.BlogConfig',  # Приложение blog
]

# Промежуточные слои (middleware) для обработки запросов/ответов
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Безопасность
    'django.contrib.sessions.middleware.SessionMiddleware',  # Сессии
    'django.middleware.common.CommonMiddleware',  # Общие функции
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware',  # Сообщения
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от clickjacking
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug toolbar
]

# Корневой URL-конфигурационный файл
ROOT_URLCONF = 'blogicum.urls'

# Директория шаблонов
TEMPLATES_DIR = BASE_DIR / 'templates'

# Конфигурация шаблонизатора Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],  # Директория для поиска шаблонов
        'APP_DIRS': True,  # Искать шаблоны в директориях приложений
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Отладка
                'django.template.context_processors.request',  # Запрос
                'django.contrib.auth.context_processors.auth',  # Аутентификация
                'django.contrib.messages.context_processors.messages',  # Сообщения
            ],
        },
    },
]

# WSGI-приложение для production-серверов
WSGI_APPLICATION = 'blogicum.wsgi.application'

# Конфигурация базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Используем SQLite
        'NAME': BASE_DIR / 'db.sqlite3',  # Путь к файлу базы данных
    }
}

# Валидаторы паролей - обеспечивают безопасность
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Языковые настройки
LANGUAGE_CODE = 'ru-RU'  # Русский язык

# Часовой пояс
TIME_ZONE = 'UTC'

# Включает поддержку интернационализации
USE_I18N = True

# Включает локализацию форматов даты/времени
USE_L10N = True

# Включает поддержку часовых поясов
USE_TZ = True

# Тип автоинкрементного поля по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL для статических файлов
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'  # Директория для статических файлов
]

# URL-адреса после успешной аутентификации
LOGIN_REDIRECT_URL = 'blog:index'  # Редирект после логина
LOGIN_URL = 'login'  # URL для страницы логина

# Настройка email-бэкенда для сохранения писем в файл
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

# Кастомный обработчик CSRF-ошибок
CSRF_FAILURE_VIEW = 'pages.views.csrf_failure'

# Настройки для медиа-файлов (изображения, документы и т.д.)
MEDIA_ROOT = BASE_DIR / 'media'  # Директория для загрузки файлов
MEDIA_URL = '/media/'  # URL для доступа к медиа-файлам