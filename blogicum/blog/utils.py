from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from blog.constants import DEFAULT_NUM_PAGE, POSTS_ON_PAGE
from blog.models import Post


def posts_pagination(request, posts):
    """
    Функция для пагинации постов.

    Args:
        request: HTTP-запрос (для получения номера страницы)
        posts: QuerySet с постами для пагинации

    Returns:
        Page: Объект страницы с постами
    """
    # Получаем номер страницы из GET-параметра, если не указан - используем DEFAULT_NUM_PAGE
    page_number = request.GET.get(
        'page',
        DEFAULT_NUM_PAGE
    )
    # Создаем объект пагинатора с заданным количеством постов на странице
    paginator = Paginator(posts, POSTS_ON_PAGE)
    # Возвращаем запрашиваемую страницу
    return paginator.get_page(page_number)


def query_post(
        manager=Post.objects,
        filters=True,
        with_comments=True
):
    """
    Функция для построения QuerySet с постами с оптимизацией запросов.

    Args:
        manager: менеджер модели (по умолчанию Post.objects)
        filters: флаг для применения фильтров (опубликованные, дата публикации)
        with_comments: флаг для добавления количества комментариев

    Returns:
        QuerySet: отфильтрованный и оптимизированный QuerySet постов
    """
    # Используем select_related для оптимизации запросов к связанным моделям
    queryset = manager.select_related('author', 'location', 'category')

    if filters:
        # Фильтруем посты: опубликованные, с датой публикации в прошлом, в опубликованной категории
        queryset = queryset.filter(
            is_published=True,
            pub_date__lt=timezone.now(),  # Дата публикации меньше текущей
            category__is_published=True
        )

    if with_comments:
        # Добавляем аннотацию с количеством комментариев к каждому посту
        queryset = queryset.annotate(comment_count=Count('comments'))

    # Сортируем по дате публикации (сначала новые)
    return queryset.order_by('-pub_date')