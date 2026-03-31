from django.contrib.auth.models import AbstractUser
from django.db import models

def user_avatar_path(instance, filename):
    # Достаем расширение исходного файла (например, .jpg или .png)
    ext = filename.split('.')[-1]
    # Формируем новое имя: avatars/ID_пользователя.расширение
    return f'avatars/user_{instance.id}.{ext}'

class User(AbstractUser):
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        verbose_name='Аватар'
    )

    def get_avatar_char(self):
        return self.username[0].upper() if self.username else '?'
    
    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"