from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Конфигурация приложения blog.

    default_auto_field: указывает тип автоинкрементного поля по умолчанию
    name: имя приложения
    verbose_name: отображаемое имя приложения в админке
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'