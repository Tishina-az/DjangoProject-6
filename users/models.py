from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True, verbose_name='Аватар')
    country = models.CharField(max_length=30, blank=True, null=True, verbose_name='Страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email
