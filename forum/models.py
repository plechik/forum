from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Thread(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название темы')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    description = models.TextField(max_length=255, verbose_name='Описание темы')
    content = models.TextField(verbose_name='Текст темы')


    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('theme_detail', kwargs={'pk': self.pk})

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts', verbose_name='Тема')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Текст сообщения')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'Сообщение от {self.author} в теме {self.thread.title}'