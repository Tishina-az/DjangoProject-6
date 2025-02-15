from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from catalog.models import Product, Contacts


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'
    top_products = Product.objects.order_by('-created_at')[:5]
    for product in top_products:
        print(product)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    fields = ['product_name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')


class ContactsTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        contact = Contacts.objects.first()
        context = {
            'contact': contact
        }
        return render(request, 'catalog/contacts.html', context=context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Поступило обращение от {name}, номер телефона:{phone}, следующего содержания: {message}.')
        return HttpResponse(f'Спасибо {name}! Ваше сообщение получено.')
