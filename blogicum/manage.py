import os
import sys


def main():
    """
    Основная функция для выполнения административных задач Django.

    Устанавливает переменную окружения для настроек Django и запускает
    командную строку Django для выполнения различных административных задач.
    """
    # Устанавливает переменную окружения для указания модуля настроек Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')

    try:
        # Импортирует функцию для выполнения команд из командной строки Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Обработка ошибки, если Django не установлен или не доступен
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Выполняет команду из командной строки (например, runserver, migrate и т.д.)
    execute_from_command_line(sys.argv)


# Проверяет, запускается ли файл напрямую (а не импортируется)
if __name__ == '__main__':
    # Запускает основную функцию, если файл запускается как скрипт
    main()