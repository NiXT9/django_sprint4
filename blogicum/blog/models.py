from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator

from blog.constants import MAX_LENGTH, MAX_TEXT, MAX_WORDS_LENGTH

User = get_user_model()


class PublishedBaseModel(models.Model):
    """
    Абстрактная модель, содержащая общие поля для публикаций.

    Поля:
    - is_published: флаг публикации (опубликовано/скрыто)
    - created_at: дата и время создания записи
    """
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        # Указывает, что модель абстрактная и не будет создаваться в базе данных
        abstract = True


class Category(PublishedBaseModel):
    """
    Модель категории для постов.

    Атрибуты:
    - title: заголовок категории
    - description: описание категории
    - slug: уникальный идентификатор для URL
    - is_published: флаг публикации (унаследовано)
    - created_at: дата создания (унаследовано)
    """
    title = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        # Настройки отображения в админке
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """
        Возвращает строковое представление объекта категории.
        Использует Truncator для ограничения количества слов.
        """
        return Truncator(self.title).words(MAX_WORDS_LENGTH)


class Location(PublishedBaseModel):
    """
    Модель местоположения для постов.

    Атрибуты:
    - name: название места
    - is_published: флаг публикации (унаследовано)
    - created_at: дата создания (унаследовано)
    """
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        """
        Возвращает строковое представление объекта местоположения.
        Использует Truncator для ограничения количества слов.
        """
        return Truncator(self.name).words(MAX_WORDS_LENGTH)


class Post(PublishedBaseModel):
    """
    Модель поста/публикации.

    Атрибуты:
    - title: заголовок поста
    - text: текст поста
    - pub_date: дата и время публикации
    - author: автор поста (связь с User)
    - location: местоположение поста (связь с Location)
    - category: категория поста (связь с Category)
    - image: изображение к посту
    - is_published: флаг публикации (унаследовано)
    - created_at: дата создания (унаследовано)
    """
    title = models.CharField(max_length=MAX_LENGTH, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.',
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении пользователя удалятся все его посты
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,  # При удалении местоположения поле станет NULL
        null=True,
        verbose_name='Местоположение',
        blank=True,  # Поле не обязательно для заполнения
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # При удалении категории поле станет NULL
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField(
        upload_to='post_images',  # Изображения будут сохраняться в папке post_images
        blank=True,
        verbose_name='Изображение к публикации'
    )

    class Meta:
        # Указывает имя связанного поля при обращении к постам через связанные модели
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        """
        Возвращает строковое представление объекта поста.
        Использует Truncator для ограничения количества слов.
        """
        return Truncator(self.title).words(MAX_WORDS_LENGTH)

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для конкретного поста.
        Используется для генерации ссылок на страницу поста.
        """
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})


class Comment(PublishedBaseModel):
    """
    Модель комментария к посту.

    Атрибуты:
    - text: текст комментария
    - author: автор комментария (связь с User)
    - post: пост, к которому относится комментарий (связь с Post)
    - is_published: флаг публикации (унаследовано)
    - created_at: дата создания (унаследовано)
    """
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении пользователя удалятся все его комментарии
        verbose_name='Автор',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # При удалении поста удалятся все комментарии к нему
        verbose_name='Комментарий',
    )

    class Meta:
        # Указывает имя связанного поля при обращении к комментариям через Post
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарий'
        ordering = ('created_at',)  # Сортировка по дате создания (сначала новые)

    def __str__(self):
        """
        Возвращает строковое представление объекта комментария.
        """
        return (f'Комментарий автора {self.author}'
                f' к посту "{self.post}",'
                f' текст: {self.text[:MAX_TEXT]}')