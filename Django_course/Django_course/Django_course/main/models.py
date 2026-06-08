# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    pub_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', verbose_name="Новость")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.user.username} - {self.news.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"