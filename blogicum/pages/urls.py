from django.urls import path
from django.views.generic.base import TemplateView

# Пространство имен для приложения pages
app_name = 'pages'

# URL-маршруты для статических страниц
urlpatterns = [
    # Страница "О проекте"
    path('about/', TemplateView.as_view(template_name='pages/about.html'),
         name='about'),
    # Страница "Правила"
    path('rules/', TemplateView.as_view(template_name='pages/rules.html'),
         name='rules'),
]