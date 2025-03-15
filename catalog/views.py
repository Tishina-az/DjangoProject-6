from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Contacts


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'
    paginate_by = 4


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
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
