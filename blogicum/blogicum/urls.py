from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

from blogicum import settings

# Обработчики ошибок
handler404 = 'pages.views.page_not_found'  # Страница 404 Not Found
handler500 = 'pages.views.server_error'  # Страница 500 Server Error

# Основные маршруты приложения
urlpatterns = [
    # Страницы приложения pages
    path('pages/', include('pages.urls', namespace='pages')),

    # Аутентификация Django (вход, выход, восстановление пароля и т.д.)
    path('auth/', include('django.contrib.auth.urls')),

    # Регистрация нового пользователя
    path('auth/registration/', CreateView.as_view(
        template_name='registration/registration_form.html',
        form_class=UserCreationForm,  # Использует стандартную форму создания пользователя
        success_url=reverse_lazy('blog:index')  # Редирект после успешной регистрации
    ),
         name='registration'),

    # Административная панель
    path('admin/', admin.site.urls),

    # Основные маршруты блога
    path('', include('blog.urls', namespace='blog')),
]

# Условие для отладочного режима - добавляет маршруты для debug_toolbar и медиа-файлов
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),  # Debug toolbar
    ]
    # Добавляет маршруты для обслуживания медиа-файлов
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )