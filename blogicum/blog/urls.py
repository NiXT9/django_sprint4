from django.urls import include, path

from blog import views

# Пространство имен для приложения blog
app_name = 'blog'

# Подмаршруты для работы с постами
posts = [
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]

# Подмаршруты для работы с профилями
profile = [
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.profile, name='profile'),
]

# Основные маршруты приложения blog
urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),  # Посты по категории
    path('posts/', include(posts)),  # Включаем подмаршруты для постов
    path('profile/', include(profile)),  # Включаем подмаршруты для профилей
]