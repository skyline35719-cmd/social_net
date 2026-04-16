from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='Уникальный адрес')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class Post(CreatedModel):
    text = models.TextField('Текст поста', help_text='Введите текст поста')
                            #validators=[not_empty])
    # pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        help_text='Выберите группу (необязательно)',
        verbose_name='Группа'
        )
    image = models.ImageField(
        'Изображение',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Post'
        verbose_name_plural  = 'Posts'
        
       
    def __str__(self):
        return self.text[:15]
    
class Comment(CreatedModel):
    post = models.ForeignKey(
            Post,
            on_delete=models.CASCADE,
            related_name='comments',
    )
    author = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='comments',
    )
    text = models.CharField('Текст комментария', max_length=300)

    def __str__(self):
        return (f'{self.text}')
    
class Follow(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="follower"
        )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="following"
        )

    class Meta:
        unique_together = ("user", "author")    
    