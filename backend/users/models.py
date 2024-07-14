from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    USER = 'user', 'Пользователь'
    ADMIN = 'admin', 'Администратор'

class CustomUser(AbstractUser):
    username = models.CharField('Имя пользователя', max_length=150, unique=True, help_text='Введите уникальное имя пользователя.')
    email = models.EmailField('Адрес электронной почты', max_length=254, unique=True, help_text='Введите действующий адрес электронной почты.')
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    role = models.CharField('Роль пользователя', max_length=30, choices=UserRole.choices, default=UserRole.USER, help_text='Выберите роль пользователя.')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers', verbose_name='Подписчик')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followings', verbose_name='Подписка')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow')
        ]

    def __str__(self):
        return f'{self.follower} подписан на {self.following}'
