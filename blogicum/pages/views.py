from django.shortcuts import render


def csrf_failure(request, reason=''):
    """
    Обработчик CSRF-ошибок.

    Args:
        request: HTTP-запрос
        reason: причина ошибки (необязательно)

    Returns:
        HttpResponse: отрендеренный шаблон страницы 403 ошибки
    """
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """
    Обработчик 404 ошибки (страница не найдена).

    Args:
        request: HTTP-запрос
        exception: исключение, вызвавшее ошибку

    Returns:
        HttpResponse: отрендеренный шаблон страницы 404 ошибки
    """
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """
    Обработчик 500 ошибки (внутренняя ошибка сервера).

    Args:
        request: HTTP-запрос

    Returns:
        HttpResponse: отрендеренный шаблон страницы 500 ошибки
    """
    return render(request, 'pages/500.html', status=500)