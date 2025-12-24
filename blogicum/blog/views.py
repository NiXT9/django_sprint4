from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import CommentForm, PostForm, ProfileForm
from blog.models import Category, Comment, Post
from blog.utils import posts_pagination, query_post


def index(request):
    """
    Отображает главную страницу с пагинированным списком опубликованных постов.

    Args:
        request: HTTP-запрос

    Returns:
        HttpResponse: Отрендеренный шаблон index.html с пагинированными постами
    """
    # Получает пагинированный список всех опубликованных постов
    page_obj = posts_pagination(request, query_post())
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def category_posts(request, category_slug):
    """
    Отображает список постов в определенной категории.

    Args:
        request: HTTP-запрос
        category_slug: слаг категории

    Returns:
        HttpResponse: Отрендеренный шаблон category.html с пагинированными постами
    """
    # Находит категорию по слагу, проверяет, что она опубликована
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    # Получает пагинированный список постов в этой категории
    page_obj = posts_pagination(
        request,
        query_post(manager=category.posts)
    )
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    """
    Отображает детали конкретного поста и форму для комментариев.

    Args:
        request: HTTP-запрос
        post_id: ID поста

    Returns:
        HttpResponse: Отрендеренный шаблон detail.html с постом и комментариями
    """
    # Если пользователь - автор поста, показывает ему все посты (включая неопубликованные)
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        # Для других пользователей показываем только опубликованные посты
        post = get_object_or_404(query_post(), id=post_id)

    # Получаем все комментарии к посту, отсортированные по дате создания
    comments = post.comments.order_by('created_at')
    # Создаем пустую форму для комментариев
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'blog/detail.html', context)


@login_required
def create_post(request):
    """
    Создает новый пост. Доступно только авторизованным пользователям.

    Args:
        request: HTTP-запрос

    Returns:
        HttpResponse: Отрендеренный шаблон create.html или редирект на профиль
    """
    # Создаем форму с данными из POST-запроса и файлами (если есть)
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        # Сохраняем пост, но не в базу данных (commit=False)
        post = form.save(commit=False)
        # Устанавливаем автора как текущего пользователя
        post.author = request.user
        # Сохраняем пост в базу данных
        post.save()
        # Редирект на страницу профиля текущего пользователя
        return redirect('blog:profile', request.user)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def edit_post(request, post_id):
    """
    Редактирует существующий пост. Доступно только автору поста.

    Args:
        request: HTTP-запрос
        post_id: ID поста для редактирования

    Returns:
        HttpResponse: Отрендеренный шаблон create.html или редирект на пост
    """
    # Находим пост по ID
    post = get_object_or_404(Post, id=post_id)
    # Проверяем, является ли текущий пользователь автором поста
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)

    # Создаем форму с данными из POST-запроса и текущими данными поста
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    """
    Удаляет пост. Доступно только автору поста.

    Args:
        request: HTTP-запрос
        post_id: ID поста для удаления

    Returns:
        HttpResponse: Отрендеренный шаблон create.html или редирект на главную
    """
    # Находим пост по ID
    post = get_object_or_404(Post, id=post_id)
    # Проверяем, является ли текущий пользователь автором поста
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)

    # Проверяем, был ли отправлен POST-запрос для подтверждения удаления
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')

    # Если GET-запрос, отображаем страницу подтверждения удаления
    form = PostForm(request.POST or None, instance=post)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


def profile(request, username):
    """
    Отображает профиль пользователя и его посты.

    Args:
        request: HTTP-запрос
        username: имя пользователя

    Returns:
        HttpResponse: Отрендеренный шаблон profile.html с профилем и постами
    """
    # Находим пользователя по имени
    profile = get_object_or_404(User, username=username)
    # Получаем посты пользователя, учитывая права доступа
    posts = query_post(manager=profile.posts, filters=profile != request.user)
    # Пагинируем посты
    page_obj = posts_pagination(request, posts)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    """
    Редактирует профиль текущего пользователя. Доступно только авторизованным.

    Args:
        request: HTTP-запрос

    Returns:
        HttpResponse: Отрендеренный шаблон user.html или редирект на профиль
    """
    # Создаем форму с данными из POST-запроса и текущими данными пользователя
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user)
    context = {'form': form}
    return render(request, 'blog/user.html', context)


@login_required
def add_comment(request, post_id):
    """
    Добавляет комментарий к посту. Доступно только авторизованным пользователям.

    Args:
        request: HTTP-запрос
        post_id: ID поста, к которому добавляется комментарий

    Returns:
        HttpResponse: Редирект на страницу поста
    """
    # Находим пост по ID
    post = get_object_or_404(Post, id=post_id)
    # Создаем форму с данными из POST-запроса
    form = CommentForm(request.POST or None)
    if form.is_valid():
        # Сохраняем комментарий, но не в базу данных
        comment = form.save(commit=False)
        # Устанавливаем пост и автора
        comment.post = post
        comment.author = request.user
        # Сохраняем комментарий в базу данных
        comment.save()
    return redirect('blog:post_detail', post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """
    Редактирует комментарий. Доступно только автору комментария.

    Args:
        request: HTTP-запрос
        post_id: ID поста
        comment_id: ID комментария для редактирования

    Returns:
        HttpResponse: Отрендеренный шаблон comment.html или редирект на пост
    """
    # Находим комментарий по ID
    comment = get_object_or_404(Comment, id=comment_id)
    # Проверяем, является ли текущий пользователь автором комментария
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)

    # Создаем форму с данными из POST-запроса и текущими данными комментария
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    context = {'form': form, 'comment': comment}
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    """
    Удаляет комментарий. Доступно только автору комментария.

    Args:
        request: HTTP-запрос
        post_id: ID поста
        comment_id: ID комментария для удаления

    Returns:
        HttpResponse: Отрендеренный шаблон comment.html или редирект на пост
    """
    # Находим комментарий по ID
    comment = get_object_or_404(Comment, id=comment_id)
    # Проверяем, является ли текущий пользователь автором комментария
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)

    # Проверяем, был ли отправлен POST-запрос для подтверждения удаления
    if request.method == "POST":
        comment.delete()
        return redirect('blog:post_detail', post_id)

    # Если GET-запрос, отображаем страницу подтверждения удаления
    context = {'comment': comment}
    return render(request, 'blog/comment.html', context)