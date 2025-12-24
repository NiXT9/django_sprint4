from django.contrib import admin

from blog.models import Category, Comment, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админская панель для модели Post.

    Поля, отображаемые в списке:
    - title: заголовок поста
    - is_published: статус публикации
    - category: категория
    - author: автор
    - location: местоположение
    - text: текст поста
    - pub_date: дата публикации
    - created_at: дата создания

    Поля, доступные для редактирования в списке:
    - is_published: можно изменить статус публикации
    - category: можно изменить категорию

    Поля для поиска: title
    Фильтры: category, is_published
    """
    list_display = (
        'title',
        'is_published',
        'category',
        'author',
        'location',
        'text',
        'pub_date',
        'created_at',
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category', 'is_published',)
    list_display_links = ('title',)  # Поле, по которому можно перейти к редактированию


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админская панель для модели Category.

    Поля, отображаемые в списке:
    - title: заголовок категории
    - is_published: статус публикации
    - slug: идентификатор для URL
    - description: описание
    - created_at: дата создания

    Поля, доступные для редактирования в списке:
    - is_published: можно изменить статус публикации
    """
    list_display = (
        'title',
        'is_published',
        'slug',
        'description',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Админская панель для модели Location.

    Поля, отображаемые в списке:
    - name: название места
    - is_published: статус публикации
    - created_at: дата создания

    Поля, доступные для редактирования в списке:
    - is_published: можно изменить статус публикации
    """
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)
    list_filter = ('is_published',)
    list_display_links = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Админская панель для модели Comment.

    Поля, отображаемые в списке:
    - text: текст комментария
    - post: пост, к которому относится комментарий
    - created_at: дата создания
    - author: автор комментария
    """
    list_display = (
        'text',
        'post',
        'created_at',
        'author'
    )


# Устанавливает отображение для пустых значений в админке
admin.site.empty_value_display = 'Не задано'