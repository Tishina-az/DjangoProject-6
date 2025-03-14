from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import BooleanField
from django.utils.safestring import mark_safe

from users.models import CustomUser


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    username = forms.CharField(label='Никнейм')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = CustomUser
        fields = (
        'email', 'username', 'first_name', 'last_name', 'phone_number', 'avatar', 'country', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Введите ваш email'
        })

        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Иван'
        })

        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Иванов'
        })

        self.fields['username'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">Обязательное поле. Не более 150 символов, содержащих только буквы, цифры и символы @/./+/-/_ .</small>')

        self.fields['avatar'].help_text = mark_safe(
            '<small id="photoHelp" class="form-text text-muted">Загрузите изображение в формате JPEG или PNG. Размер не должен превышать 5 МБ.</small>')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона может состоять только из цифр.')
        return phone_number
