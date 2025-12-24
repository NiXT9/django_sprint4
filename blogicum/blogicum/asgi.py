import os

from django.core.asgi import get_asgi_application

# Устанавливает переменную окружения для указания модуля настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')

# Создает ASGI-приложение Django
application = get_asgi_application()