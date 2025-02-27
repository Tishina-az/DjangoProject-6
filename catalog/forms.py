import logging

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import BooleanField

from catalog.models import Product

logger = logging.getLogger(__name__)

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар', ]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['created_at', 'updated_at']

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        logger.debug(f'Очищенное название продукта: {product_name}')
        if product_name:
            for word in FORBIDDEN_WORDS:
                if word in product_name.lower():
                    logger.error(f'Обнаружено запрещенное слово: {word}')
                    raise ValidationError(f'Недопустимо использовать "{word}" в названии продукта')
        else:
            logger.error('Название продукта отсутствует или пустое')
            raise ValidationError('Название продукта обязательно для заполнения.')
        return product_name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        logger.debug(f'Очищенное описание продукта: {description}')
        if description:
            for word in FORBIDDEN_WORDS:
                if word in description.lower():
                    logger.error(f'Обнаружено запрещенное слово: {word}')
                    raise ValidationError(f'Недопустимо использовать "{word}" в описании продукта')
        else:
            logger.error('Описание продукта отсутствует или пустое')
            raise ValidationError('Описание продукта обязательно для заполнения.')
        return description

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')
        description = cleaned_data.get('description')

        logger.debug(f'Очищенные данные: {cleaned_data}')
        if not product_name:
            logger.error('Поле product_name отсутствует или пустое')
            raise ValidationError({'product_name': 'Это поле обязательно для заполнения.'})
        if not description:
            logger.error('Поле description отсутствует или пустое')
            raise ValidationError({'description': 'Это поле обязательно для заполнения.'})

        return cleaned_data
