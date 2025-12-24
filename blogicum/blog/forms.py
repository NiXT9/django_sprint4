from django import forms

from blog.models import Comment, Post, User


class CommentForm(forms.ModelForm):
    """
    Форма для создания и редактирования комментариев.
    """
    class Meta:
        model = Comment
        fields = ('text',)  # Разрешаем редактировать только текст комментария


class PostForm(forms.ModelForm):
    """
    Форма для создания и редактирования постов.
    """
    class Meta:
        model = Post
        exclude = ('author',)  # Исключаем поле автора из формы (устанавливается автоматически)
        widgets = {
            # Используем специальный виджет для даты и времени
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}  # HTML5 input для выбора даты и времени
            )
        }


class ProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя.
    """
    class Meta:
        model = User
        # Поля, которые можно редактировать в профиле
        fields = ('username', 'first_name', 'last_name', 'email')