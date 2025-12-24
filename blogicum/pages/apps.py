from django.apps import AppConfig


class PagesConfig(AppConfig):
    """
    Конфигурация приложения pages.

    default_auto_field: указывает тип автоинкрементного поля по умолчанию
    name: имя приложения
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'