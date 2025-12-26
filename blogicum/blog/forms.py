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

    class Meta:
        model = Post
        exclude = ('author', 'created_at')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}
            ),
            'is_published': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }

        labels = {
            'is_published': 'Опубликовать пост'
        }
        help_texts = {
            'is_published': 'Снимите галочку, чтобы скрыть публикацию'
        }


class ProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя.
    """
    class Meta:
        model = User
        # Поля, которые можно редактировать в профиле
        fields = ('username', 'first_name', 'last_name', 'email')