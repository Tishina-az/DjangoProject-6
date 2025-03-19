from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Наименование категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание категории')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['category_name', ]


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='Наименование продукта')
    description = models.TextField(blank=True, null=True, verbose_name='Описание продукта')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products', verbose_name='Категория')
    price = models.IntegerField(null=False, verbose_name='Стоимость продукта')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    is_publication = models.BooleanField(default=False, verbose_name='Статус публикации')

    def __str__(self):
        return f'{self.product_name} - {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['product_name', ]
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
        ]


class Contacts(models.Model):
    country = models.CharField(max_length=50, null=False, verbose_name='Страна')
    address = models.CharField(max_length=200, null=False, verbose_name='Адрес')
    phone = models.CharField(max_length=20, default='+7(999)-999-99-99', verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Адрес электронной почты')

    def __str__(self):
        return f'Адрес: {self.country}, {self.address}. Телефон: {self.phone}.'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['country', ]
