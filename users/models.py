from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона',
                                    help_text='Необязательное поле. Введите ваш номер телефона.')
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True, verbose_name='Аватар',
                               help_text='Загрузите изображение.')
    country = models.CharField(max_length=30, blank=True, null=True, verbose_name='Страна')
    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
