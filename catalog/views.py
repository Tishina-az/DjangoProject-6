from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product


def home(request):
    """ Отображение главное страницы каталога """
    top_products = Product.objects.order_by('-created_at')[:5]
    for product in top_products:
        print(product)
    return render(request, 'catalog/home.html')


def contacts(request):
    """ Отображение страницы Контакты и форма обратной связи """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Поступило обращение от {name}, номер телефона:{phone}, следующего содержания: {message}.')
        return HttpResponse(f'Спасибо {name}! Ваше сообщение получено.')
    return render(request, 'catalog/contacts.html')
