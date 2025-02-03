from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Наименование категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание категории')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name', ]


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='Наименование продукта')
    description = models.TextField(blank=True, null=True, verbose_name='Описание продукта')
    image = models.ImageField(upload_to='catalog/images', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    price = models.IntegerField(null=False, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.product_name} - {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name', ]
