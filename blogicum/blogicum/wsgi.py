import os

from django.core.wsgi import get_wsgi_application

# Устанавливает переменную окружения для указания модуля настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')

# Создает WSGI-приложение Django
application = get_wsgi_application()