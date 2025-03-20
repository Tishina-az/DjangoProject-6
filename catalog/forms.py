from django import forms
from django.core.exceptions import ValidationError
from django.db.models import BooleanField
from django.utils.safestring import mark_safe

from catalog.models import Product


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
        exclude = ['created_at', 'updated_at', 'is_publication', 'owner']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['product_name'].widget.attrs.update({
            'placeholder': 'Введите название продукта'
        })

        self.fields['description'].widget.attrs.update({
            'placeholder': 'Добавьте описание продукта...'
        })

        self.fields['image'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">Загрузите изображение в формате JPEG или PNG. Размер не должен превышать 5 МБ.</small>')

        self.fields['category'].empty_label = 'Выберите категорию...'

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if product_name:
            for word in FORBIDDEN_WORDS:
                if word in product_name.lower():
                    raise ValidationError(f'Недопустимо использовать "{word}" в названии продукта')
        else:
            raise ValidationError('Название продукта обязательно для заполнения.')
        return product_name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            for word in FORBIDDEN_WORDS:
                if word in description.lower():
                    raise ValidationError(f'Недопустимо использовать "{word}" в описании продукта')
        else:
            raise ValidationError('Описание продукта обязательно для заполнения.')
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            valid_formats = ['image/jpeg', 'image/png']
            if image.content_type not in valid_formats:
                raise ValidationError('Формат файла должен быть JPEG или PNG.')

            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError('Размер файла не должен превышать 5 МБ.')
        return image

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price:
            if price < 0:
                raise ValidationError('Стоимость продукта не может быть меньше нуля')
        else:
            raise ValidationError('Стоимость продукта обязательна для заполнения.')
        return price

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')
        description = cleaned_data.get('description')

        if not product_name:
            raise ValidationError({'product_name': 'Это поле обязательно для заполнения.'})
        if not description:
            raise ValidationError({'description': 'Это поле обязательно для заполнения.'})

        return cleaned_data
