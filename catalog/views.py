from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product, Contacts


def home(request):
    """ Отображение главное страницы каталога """
    top_products = Product.objects.order_by('-created_at')[:5]
    for product in top_products:
        print(product)
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'catalog/home.html', context)


def product_detail(request, pk):
    """ Отображение страницы товара """
    product = Product.objects.get(pk=pk)
    context = {
        'product': product
    }
    return render(request, 'catalog/product.html', context)


def contacts(request):
    """ Отображение страницы Контакты и форма обратной связи """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Поступило обращение от {name}, номер телефона:{phone}, следующего содержания: {message}.')
        return HttpResponse(f'Спасибо {name}! Ваше сообщение получено.')
    contact = Contacts.objects.first()
    context = {
        'contact': contact
    }
    return render(request, 'catalog/contacts.html', context=context)
