from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое поста')
    preview = models.ImageField(upload_to='preview/', blank=True, null=True, verbose_name='Превью')
    created_at = models.DateField(auto_now_add=True, editable=False, verbose_name='Дата создания')
    publication_at = models.BooleanField(default=False, verbose_name='Признак публикации')
    number_of_views = models.PositiveIntegerField(default=0, editable=False, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title} - {self.created_at}\nКоличество просмотров: {self.number_of_views}.'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at', ]
